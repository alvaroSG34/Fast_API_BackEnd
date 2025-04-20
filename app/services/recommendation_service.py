from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from fastapi import HTTPException
import traceback

from app.models.product import Product
from app.models.sale import Venta
from app.models.sale_detail import DetalleVenta

# Función principal para obtener recomendaciones basadas en un producto
def get_recommendations_for_product(db: Session, product_id: int, max_recommendations: int = 4):
    """
    Genera recomendaciones para un producto específico utilizando el algoritmo Apriori
    """
    try:
        # Verificar que el producto existe
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Obtener las reglas de asociación
        rules_df = _generate_association_rules(db)
        
        if rules_df.empty:
            # Si no hay suficientes datos para generar reglas, usar recomendaciones por categoría
            return get_recommendations_by_category(db, product_id, max_recommendations)
        
        # Filtrar las reglas donde el producto actual está en los antecedentes
        product_recommendations = rules_df[rules_df['antecedents'].apply(lambda x: product_id in x)]
        
        if product_recommendations.empty:
            # Si no hay recomendaciones específicas para este producto
            return get_recommendations_by_category(db, product_id, max_recommendations)
        
        # Ordenar por la métrica lift (mayor relevancia)
        product_recommendations = product_recommendations.sort_values('lift', ascending=False)
        
        # Extraer los IDs de productos recomendados
        recommended_product_ids = []
        for _, row in product_recommendations.iterrows():
            for prod_id in row['consequents']:
                if prod_id not in recommended_product_ids and prod_id != product_id:
                    recommended_product_ids.append(prod_id)
                    if len(recommended_product_ids) >= max_recommendations:
                        break
            if len(recommended_product_ids) >= max_recommendations:
                break
        
        # Si no tenemos suficientes recomendaciones, complementar con productos de la misma categoría
        if len(recommended_product_ids) < max_recommendations:
            category_recommendations = get_recommendations_by_category(
                db, product_id, max_recommendations - len(recommended_product_ids)
            )
            # Filtrar para evitar duplicados
            for rec in category_recommendations:
                if rec['id'] not in recommended_product_ids and rec['id'] != product_id:
                    recommended_product_ids.append(rec['id'])
                    if len(recommended_product_ids) >= max_recommendations:
                        break
        
        # Obtener los detalles completos de los productos recomendados
        recommended_products = []
        for prod_id in recommended_product_ids:
            product = db.query(Product).filter(Product.id == prod_id).first()
            if product:
                recommended_products.append({
                    "id": product.id,
                    "nombre": product.nombre,
                    "precio_venta": product.precio_venta,
                    "imagen": product.imagen,
                    "id_categoria": product.id_categoria
                })
        
        return recommended_products
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_recommendations_for_product: {str(e)}")
        print(traceback.format_exc())
        # En caso de error, devolver recomendaciones alternativas
        return get_recommendations_by_category(db, product_id, max_recommendations)

# Función para generar las reglas de asociación usando Apriori
def _generate_association_rules(db: Session, min_support=0.01, min_confidence=0.1):
    """
    Genera reglas de asociación a partir del historial de ventas usando Apriori
    """
    try:
        # Obtener todas las ventas y sus detalles
        ventas = db.query(Venta).filter(Venta.estado == 'completada').all()
        
        if not ventas:
            return pd.DataFrame()  # No hay datos suficientes
            
        # Crear un dataframe con las transacciones (venta_id, producto_id)
        transactions = []
        for venta in ventas:
            detalles = db.query(DetalleVenta).filter(DetalleVenta.id_venta == venta.id_venta).all()
            if detalles:
                transaction = {
                    'venta_id': venta.id_venta,
                    'productos': [detalle.id_producto for detalle in detalles]
                }
                transactions.append(transaction)
        
        if not transactions:
            return pd.DataFrame()  # No hay datos suficientes
            
        # Crear matriz de incidencia (cada fila es una venta, cada columna es un producto)
        # 1 si el producto está en la venta, 0 en caso contrario
        all_products = set()
        for t in transactions:
            all_products.update(t['productos'])
        
        # Crear la matriz de incidencia
        basket = pd.DataFrame(0, index=range(len(transactions)), 
                             columns=list(all_products))
        
        for i, t in enumerate(transactions):
            basket.loc[i, t['productos']] = 1
        
        # Aplicar Apriori para encontrar conjuntos frecuentes
        frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
        
        if frequent_itemsets.empty:
            return pd.DataFrame()  # No hay conjuntos frecuentes suficientes
            
        # Generar reglas de asociación
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        
        if rules.empty:
            return pd.DataFrame()  # No hay reglas suficientes
            
        # Convertir los frozensets a listas para facilitar su manejo
        rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
        rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
        
        return rules
        
    except Exception as e:
        print(f"Error en _generate_association_rules: {str(e)}")
        print(traceback.format_exc())
        return pd.DataFrame()  # En caso de error devolver un dataframe vacío

# Función alternativa para obtener recomendaciones por categoría
def get_recommendations_by_category(db: Session, product_id: int, max_recommendations: int = 4):
    """
    Genera recomendaciones basadas en la categoría del producto
    Útil cuando no hay suficientes datos para el algoritmo Apriori
    """
    try:
        # Obtener el producto actual
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Obtener otros productos de la misma categoría
        similar_products = db.query(Product).filter(
            Product.id_categoria == product.id_categoria,
            Product.id != product_id,
            Product.estado == 'activo'  # Asumiendo que los productos tienen un campo 'estado'
        ).limit(max_recommendations).all()
        
        # Si no hay suficientes productos en la misma categoría, obtener productos populares
        if len(similar_products) < max_recommendations:
            # Complementar con productos de otras categorías (los más vendidos)
            popular_products = db.query(Product, db.func.count(DetalleVenta.id_producto).label('count'))\
                .join(DetalleVenta, DetalleVenta.id_producto == Product.id)\
                .filter(Product.id != product_id)\
                .filter(Product.id_categoria != product.id_categoria)\
                .group_by(Product.id)\
                .order_by(db.desc('count'))\
                .limit(max_recommendations - len(similar_products))\
                .all()
            
            # Agregar productos populares a la lista
            similar_products.extend([p[0] for p in popular_products])
        
        # Formatear la respuesta
        recommendations = []
        for p in similar_products:
            recommendations.append({
                "id": p.id,
                "nombre": p.nombre,
                "precio_venta": p.precio_venta,
                "imagen": p.imagen,
                "id_categoria": p.id_categoria
            })
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_recommendations_by_category: {str(e)}")
        print(traceback.format_exc())
        
        # En caso de error, intentar devolver algunos productos aleatorios
        try:
            random_products = db.query(Product).filter(
                Product.id != product_id
            ).order_by(db.func.random()).limit(max_recommendations).all()
            
            return [{
                "id": p.id,
                "nombre": p.nombre,
                "precio_venta": p.precio_venta,
                "imagen": p.imagen,
                "id_categoria": p.id_categoria
            } for p in random_products]
            
        except:
            return []  # Si todo falla, devolver lista vacía

# Función para obtener recomendaciones basadas en el carrito actual
def get_recommendations_for_cart(db: Session, cart_item_ids: list, max_recommendations: int = 4):
    """
    Genera recomendaciones basadas en los productos que ya están en el carrito
    """
    try:
        if not cart_item_ids:
            # Si el carrito está vacío, devolver productos populares
            popular_products = db.query(Product, db.func.count(DetalleVenta.id_producto).label('count'))\
                .join(DetalleVenta, DetalleVenta.id_producto == Product.id)\
                .group_by(Product.id)\
                .order_by(db.desc('count'))\
                .limit(max_recommendations)\
                .all()
                
            return [{
                "id": p[0].id,
                "nombre": p[0].nombre,
                "precio_venta": p[0].precio_venta,
                "imagen": p[0].imagen,
                "id_categoria": p[0].id_categoria
            } for p in popular_products]
        
        # Obtener las reglas de asociación
        rules_df = _generate_association_rules(db)
        
        if rules_df.empty:
            # Si no hay suficientes datos para reglas, usar el algoritmo más simple
            return get_diverse_recommendations(db, cart_item_ids, max_recommendations)
        
        # Para cada producto en el carrito, encontrar productos recomendados
        all_recommendations = []
        recommended_ids = set()
        
        for product_id in cart_item_ids:
            # Filtrar reglas donde el producto actual está en los antecedentes
            product_rules = rules_df[rules_df['antecedents'].apply(lambda x: product_id in x)]
            
            if not product_rules.empty:
                # Ordenar por la métrica lift (mayor relevancia)
                product_rules = product_rules.sort_values('lift', ascending=False)
                
                # Extraer los IDs de productos recomendados
                for _, row in product_rules.iterrows():
                    for rec_id in row['consequents']:
                        if rec_id not in cart_item_ids and rec_id not in recommended_ids:
                            recommended_ids.add(rec_id)
                            all_recommendations.append(rec_id)
                            if len(all_recommendations) >= max_recommendations:
                                break
                    if len(all_recommendations) >= max_recommendations:
                        break
        
        # Si no tenemos suficientes recomendaciones, complementar con productos diversos
        if len(all_recommendations) < max_recommendations:
            diverse_recs = get_diverse_recommendations(
                db, 
                cart_item_ids, 
                max_recommendations - len(all_recommendations)
            )
            
            # Agregar solo los que no están ya recomendados
            for rec in diverse_recs:
                if rec['id'] not in recommended_ids and rec['id'] not in cart_item_ids:
                    all_recommendations.append(rec['id'])
                    if len(all_recommendations) >= max_recommendations:
                        break
        
        # Obtener los detalles completos de los productos recomendados
        final_recommendations = []
        for rec_id in all_recommendations[:max_recommendations]:
            product = db.query(Product).filter(Product.id == rec_id).first()
            if product:
                final_recommendations.append({
                    "id": product.id,
                    "nombre": product.nombre,
                    "precio_venta": product.precio_venta,
                    "imagen": product.imagen,
                    "id_categoria": product.id_categoria
                })
        
        return final_recommendations
        
    except Exception as e:
        print(f"Error en get_recommendations_for_cart: {str(e)}")
        print(traceback.format_exc())
        # En caso de error, devolver recomendaciones alternativas
        return get_diverse_recommendations(db, cart_item_ids, max_recommendations)

# Función para obtener recomendaciones diversas 
def get_diverse_recommendations(db: Session, exclude_ids: list, max_recommendations: int = 4):
    """
    Genera recomendaciones diversas de diferentes categorías
    Útil cuando no hay suficientes datos para el algoritmo Apriori
    """
    try:
        # Obtener las categorías de los productos a excluir
        exclude_categories = []
        if exclude_ids:
            products = db.query(Product).filter(Product.id.in_(exclude_ids)).all()
            exclude_categories = [p.id_categoria for p in products]
        
        # Primero, obtener productos de categorías diferentes a las de los productos excluidos
        diverse_products = []
        
        if exclude_categories:
            diverse_query = db.query(Product)\
                .filter(Product.id.notin_(exclude_ids))\
                .filter(Product.id_categoria.notin_(exclude_categories))\
                .order_by(db.func.random())\
                .limit(max_recommendations // 2)
                
            diverse_products = diverse_query.all()
        
        # Completar con productos populares
        remaining = max_recommendations - len(diverse_products)
        if remaining > 0:
            popular_query = db.query(Product, db.func.count(DetalleVenta.id_producto).label('count'))\
                .join(DetalleVenta, DetalleVenta.id_producto == Product.id)\
                .filter(Product.id.notin_(exclude_ids))\
                .group_by(Product.id)\
                .order_by(db.desc('count'))\
                .limit(remaining)
                
            popular_products = [p[0] for p in popular_query.all()]
            diverse_products.extend(popular_products)
        
        # Si aún no tenemos suficientes, añadir algunos productos aleatorios
        remaining = max_recommendations - len(diverse_products)
        if remaining > 0:
            random_query = db.query(Product)\
                .filter(Product.id.notin_(exclude_ids))\
                .filter(Product.id.notin_([p.id for p in diverse_products]))\
                .order_by(db.func.random())\
                .limit(remaining)
                
            random_products = random_query.all()
            diverse_products.extend(random_products)
        
        # Formatear la respuesta
        recommendations = []
        for p in diverse_products:
            recommendations.append({
                "id": p.id,
                "nombre": p.nombre,
                "precio_venta": p.precio_venta,
                "imagen": p.imagen,
                "id_categoria": p.id_categoria
            })
        
        return recommendations
        
    except Exception as e:
        print(f"Error en get_diverse_recommendations: {str(e)}")
        print(traceback.format_exc())
        return []  # En caso de error, devolver lista vacía 