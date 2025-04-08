# **PARTE II \- PROCESO UNIFICADO DE DESARROLLO DE SOFTWARE** {#parte-ii---proceso-unificado-de-desarrollo-de-software}

2. # **FLUJO DE TRABAJO CAPTURA REQUISITOS** {#flujo-de-trabajo-captura-requisitos}

   1. ## **Flujo de Trabajo: Captura de Requisitos** {#flujo-de-trabajo:-captura-de-requisitos}

      1. ### IDENTIFICAR ACTORES Y CASOS DE USO {#identificar-actores-y-casos-de-uso}

###  **Actores del Sistema** {#actores-del-sistema}

Los actores son todas aquellas entidades externas que interactúan con el sistema, ya sean personas o sistemas externos.

En tu proyecto, estos actores podrían ser:

1. **Cliente:** Persona que realiza la compra usando la aplicación web o móvil.

2. **Vendedor (Cajero):** Usuario del sistema encargado de realizar y gestionar ventas.

3. **Administrador:** Usuario con control total del sistema, gestiona inventario, productos, usuarios y roles, y genera reportes.

4. **Supervisor de Inventario (Almacén):** Usuario encargado de gestionar y supervisar los niveles de inventario.

5. **Pasarela de Pago:** Sistema externo (Libélula, Stripe, etc.) que gestiona y procesa pagos en línea.

6. **Motor de Reconocimiento de Voz:** Sistema externo (Google Cloud Speech-to-Text, Vosk, etc.) que procesa comandos de voz.  
   

###  **Tabla resumen (Actores ↔ Casos de Uso)** {#tabla-resumen-(actores-↔-casos-de-uso)}

| Actores | Casos de Uso principales |
| ----- | ----- |
| Cliente | Realizar compra, recibir recomendaciones |
| Vendedor (Cajero) | Registrar ventas, aplicar descuentos, cobrar |
| Administrador | Gestión de productos, usuarios, inventario, generación de reportes |
| Supervisor de Inventario | Monitorear inventario, recibir notificaciones |
| Pasarela de Pago | Procesar pagos online |
| Motor de Reconocimiento Voz | Capturar y traducir comandos de voz |

###  **Casos de Uso del Sistema** {#casos-de-uso-del-sistema}

Los casos de uso describen las funcionalidades o acciones específicas que pueden realizar los actores con el sistema. Aquí identificamos los principales casos de uso según el alcance y los requisitos especificados:

#### **Gestión de Ventas** {#gestión-de-ventas}

* CU1 Registrar productos en el carrito (por teclado, mouse o voz).

* CU2 Calcular el total de la compra.

* CU3 Aplicar descuentos.

* CU4 Realizar pago mediante pasarela de pago.

* CU5 Generar recibo digital de la compra.

####  **Recomendaciones Inteligentes** {#recomendaciones-inteligentes}

* CU6 Generar recomendaciones automáticas basadas en transacciones históricas.

* CU7 Mostrar productos recomendados durante la compra en tiempo real.

####  **Reconocimiento de Voz** {#reconocimiento-de-voz}

* CU8 Capturar comandos de voz del usuario.

* CU9 Procesar y traducir comandos de voz a texto.

* CU10 Ejecutar comandos interpretados (agregar productos, calcular total, etc.).

* CU11 Confirmar verbalmente o visualmente acciones realizadas.

####  **Gestión de Inventario** {#gestión-de-inventario}

* CU12 Registrar nuevos productos.

* CU13 Editar información de productos.

* CU14 Eliminar productos del inventario.

* CU15 Monitorear niveles de inventario.

* CU16 Notificar automáticamente al supervisor cuando el stock sea bajo.

####  **Generación de Reportes** {#generación-de-reportes}

* CU17 Generar reporte de ventas por cliente en un periodo específico.

* CU18 Generar reporte de productos más vendidos.

* CU19 Exportar reportes generados en formatos PDF y Excel.

####  **Gestión de Usuarios y Roles** {#gestión-de-usuarios-y-roles}

* CU20 Registrar nuevos usuarios.

* CU21 Asignar roles específicos (administrador, vendedor, supervisor).

* CU22 Editar o eliminar usuarios existentes.

  2. ### PRIORIZAR CASOS DE USO {#priorizar-casos-de-uso}

Iteracion 1  
Iteracion 2  
Iteracion 3  
Iteracion 4

| ID | CASO DE USO | ESTADO | PRIORIDAD | RIESGO | ACTOR |
| :---- | :---- | :---- | :---- | :---- | :---- |
| CU1 | Registrar productos en el carrito. | Propuesto | Alta | Bajo | Vendedor, Cliente |
| CU2 | Calcular total de la compra | Propuesto | Alta | Bajo | Vendedor, Cliente |
| CU3 | Aplicar descuentos | Propuesto | Medio | Bajo | Vendedor |
| CU4 | Realizar pago mediante pasarela | Propuesto | Alta | Medio | Cliente, Pasarela de pago |
| CU5 | Generar recibo digital | Propuesto | Alta | Bajo | Vendedor, Cliente |
| CU6 | Generar recomendaciones inteligentes | Propuesto | Alta | Alto | Cliente |
| CU8 | Capturar comandos de voz | Propuesto | Alta | Alto | Cliente, Motor de voz |
| CU9 | Procesar comandos de voz | Propuesto | Alta | Alto | Motor Voz |
| CU10 | Ejecutar acciones por comandos de voz | Propuesto | Alta | Medio | Cliente, Motor Voz |
| Cu11 | Confirmar acciones realizadas | Propuesto | Media | Bajo | Cliente, Motor Voz |
| CU12 | Registrar nuevos productos | Propuesto | Alta | Bajo | Administrador |
| CU13 | Editar información de productos | Propuesto | Media | Bajo | Administrador |
| CU14 | Eliminar productos de inventario | Propuesto | Media | Bajo | Administrador |
| CU15 | Monitorear niveles de inventario | Propuesto | Alta | Medio | Supervisor Inventario |
| CU16 | Notificar  bajo stock automáticamente | Propuesto | Alta | Medio | Supervisor Inventario |
| CU17 | Generar reportes por cliente | Propuesto | Media | Bajo | Administrador |
| CU18 | Generar reportes productos más vendidos | Propuesto | Media | Bajo | Administrador |
| CU19 | Exportar reportes en pdf y Excel | Propuesto | Alta | Medio | Administrador |
| CU20 | Registrar usuarios (Interno) | Propuesto | Alta | Bajo | Administrador |
| CU21 | Asignar roles a usuarios | Propuesto | Alta | Bajo | Administrador |
| CU22 | Editar o eliminar usuarios existentes | Propuesto | Medio | Bajo | Administrador |
| CU23 | Inicio de Sesión | Propuesto | Alta | Bajo | Todos los usuarios |
| CU24 | Cerrar Sesión | Propuesto | Alta | Bajo | Todos los usuarios |
| CU25 | Registro Usuario (Cliente) | Propuesto | Alta | Bajo | Cliente |

### Iteración 1 – Autenticación y flujo básico de ventas {#iteración-1-–-autenticación-y-flujo-básico-de-ventas}

| ID | Caso de Uso | Actor |
| :---- | :---- | :---- |
| CU23 | Inicio de Sesión | Cliente, Vendedor, Administrador, Supervisor  |
| CU24 | Cerrar Sesión | Cliente, Vendedor, Administrador, Supervisor  |
| CU25 | Registro Usuario (Cliente) | Cliente |
| CU20 | Registrar usuarios (Interno) | Administrador |
| CU12 | Registrar nuevos productos | Administrador |
| CU21 | Asignar roles a usuarios | Administrador |

### Iteración 2 – Administración e inventario {#iteración-2-–-administración-e-inventario}

| ID | Caso de Uso | Actor |
| :---- | :---- | :---- |
| CU1 | Registrar productos en el carrito | Vendedor, Cliente |
| CU13 | Editar información de productos | Administrador |
| CU14 | Eliminar productos de inventario | Administrador |
| CU15 | Monitorear niveles de inventario | Supervisor Inventario |
| CU16 | Notificar bajo stock automáticamente | Supervisor Inventario |
| CU5 | Generar recibo digital | Vendedor, Cliente |
| CU22 | Editar o eliminar usuarios existentes | Administrador |
| CU3 | Aplicar descuentos | Vendedor |
| CU2 | Calcular total de la compra | Vendedor, Cliente |

### Iteración 3 – Reportes y recomendaciones {#iteración-3-–-reportes-y-recomendaciones}

| ID | Caso de Uso | Actor |
| :---- | :---- | :---- |
| CU6 | Generar recomendaciones inteligentes | Cliente |
| CU17 | Generar reportes por cliente | Administrador |
| CU18 | Generar reportes productos más vendidos | Administrador |
| CU19 | Exportar reportes en PDF y Excel | Administrador |

### Iteración 4 – Reconocimiento de voz y pagos {#iteración-4-–-reconocimiento-de-voz-y-pagos}

| ID | Caso de Uso | Actor |
| :---- | :---- | :---- |
| CU4 | Realizar pago mediante pasarela | Cliente, Pasarela de pago |
| CU8 | Capturar comandos de voz | Cliente, Motor de voz |
| CU9 | Procesar comandos de voz | Motor Voz |
| CU10 | Ejecutar acciones por comandos de voz | Cliente, Motor Voz |
| CU11 | Confirmar acciones realizadas | Cliente, Motor Voz |

3. ### DETALLAR CASOS DE USO {#detallar-casos-de-uso}

### Iteración 1 {#iteración-1}

**CU23 Inicio de Sesión**

![][image1]

| Caso de uso | CU23. INICIAR SESIÓN |
| :---- | :---- |
| **Propósito** | Validar el inicio de sesión de un usuario para acceder al sistema web. |
| **Actores** | Cliente,Administrador,Supervisor,Vendedor |
| **Actor Iniciador** | Cliente,Administrador,Supervisor,Vendedor |
| **Precondición** | El usuario debe estar registrado en el sistema |
| **Flujo Principal** | ***1***. El usuario abre la aplicación o sistema web. 2\. Selecciona la opción “Iniciar sesión”. 3\. Ingresa su correo/usuario y contraseña. 4\. El sistema valida las credenciales. 5\. Si son correctas, se permite el acceso al sistema. 6\. El sistema redirige al usuario a la pantalla principal correspondiente a su rol. |
| **Postcondición** | El usuario queda autenticado dentro del sistema. |
| **Excepción** | Error de conexión o servidor caído: |

**CU.24 Cerrar Sesión**

![][image2]

| Caso de uso | CU24. Cerrar Sesión |
| :---- | :---- |
| **Propósito** | Permite al usuario salir del sistema y finalizar su sesión activa. |
| **Actores** | Cliente,Administrador,Supervisor,Vendedor |
| **Actor Iniciador** | Cliente,Administrador,Supervisor,Vendedor |
| **Precondición** | El usuario debe haber iniciado sesión previamente. |
| **Flujo Principal** | 1\. El usuario accede a la opción “Cerrar sesión”. 2\. El sistema solicita confirmación (opcional). 3\. El usuario confirma. 4\. El sistema invalida la sesión activa. 5\. El usuario es redirigido a la pantalla de inicio o login.  |
| **Postcondición** | La sesión del usuario queda cerrada. |
| **Excepción** | Error en el cierre de sesión (problema de red o token inválido) |

**CU.25  Registro Usuario (Cliente)**

![][image3]

| Caso de uso | CU 25\. Registro Usuario |
| :---- | :---- |
| **Propósito** | Permite al cliente registrarse en el sistema. |
| **Actores** | Cliente |
| **Actor Iniciador** | Cliente |
| **Precondición** | Ninguna |
| **Flujo Principal** | 1\. El Cliente accede a la pantalla de registro. 2\. Ingresa los datos requeridos (nombre, email, contraseña, etc.). 3\. El sistema valida los datos. 4\. Si todo está correcto, se crea la cuenta. 5\. El usuario es redirigido a la pantalla de home de la página.  |
| **Postcondición** | El nuevo usuario queda registrado en la base de datos. |
| **Excepción** | Problemas de red o fallo del servidor: el sistema muestra un mensaje de error. |

**CU.20 Registrar usuarios (Interno)**

![][image4]

| Caso de uso | CU 25\. Registrar Usuarios |
| :---- | :---- |
| **Propósito** | Permite al Administrador registrar un nuevo usuario en el sistema y asignarle un rol determinado. |
| **Actores** | Administrador |
| **Actor Iniciador** | Administrador |
| **Precondición** | Debe tener permisos para gestionar usuarios. |
| **Flujo Principal** | 1\. El administrador accede a la opción “Crear usuario”. 2\. Completa el formulario con los datos personales del nuevo usuario. 3\. El sistema valida los datos. 4\. El administrador selecciona el rol correspondiente (Empleado, Supervisor, etc.). 5\. El sistema guarda los datos y crea la cuenta. 6\. El sistema envía una notificación (correo o mensaje) al nuevo usuario.  |
| **Postcondición** | El nuevo usuario queda registrado en el sistema con el rol asignado. |
| **Excepción** | El sistema muestra un mensaje y detiene el proceso. |

**CU 12 Registrar Nuevos Productos**

![][image5]

| Caso de uso | CU 25\. Registrar Nuevos Productos |
| :---- | :---- |
| **Propósito** | Permite registrar un nuevo producto en el sistema, incluyendo su información básica y archivos multimedia como imágenes. |
| **Actores** | Administrador, Supervisor |
| **Actor Iniciador** | Administrador,Supervisor |
| **Precondición** | Debe tener permisos para gestionar productos. |
| **Flujo Principal** | 1\. El administrador accede al módulo de productos. 2\. Selecciona la opción “Registrar nuevo producto”. 3\. Completa los campos requeridos (nombre, categoría, descripción, precio, etc.). 4\. Adjunta imágenes relacionadas (opcional o requerido). 5\. Confirma la creación del producto. 6\. El sistema guarda la información y muestra mensaje de éxito.  |
| **Postcondición** | El nuevo producto queda disponible en el sistema para su visualización o gestión posterior. |
| **Excepción** | El sistema muestra un mensaje y detiene el proceso. |

**CU21 Asignar Roles a usuarios**

![][image6]

| Caso de uso | CU 21\. Asignar Roles a usuarios |
| :---- | :---- |
| **Propósito** | Permite al administrador del sistema asignar un rol (Ej. Empleado, Supervisor) a un usuario existente, para definir sus permisos y accesos. |
| **Actores** | Administrador |
| **Actor Iniciador** | Administrador |
| **Precondición** | El usuario a modificar debe existir. El administrador debe tener permisos para asignar roles. |
| **Flujo Principal** | 1\. El administrador accede al módulo de usuarios. 2\. Busca al usuario deseado. 3\. Selecciona la opción “Asignar rol”. 4\. Elige el rol deseado de una lista. 5\. Confirma la acción. 6\. El sistema guarda los cambios y muestra un mensaje de éxito.  |
| **Postcondición** | El usuario queda con el nuevo rol asignado. |
| **Excepción** | No se actualiza el rol y se muestra mensaje de error. |

### Iteración 2 {#iteración-2}

CU1. Registrar productos en el carrito

![][image7]

| Caso de uso | CU1. Registrar productos en el carrito |
| :---- | :---- |
| **Propósito** | Permite al cliente mover un producto a una lista de compras, un carrito de compras, para iniciar un proceso de compra. |
| **Actores** | Vendedor, Cliente |
| **Actor Iniciador** | Vendedor o Cliente |
| **Precondición** | El usuario debe haber iniciado sesion en el sistema, y tambien debe existir un catalogo existente de productos disponibles. |
| **Flujo Principal** | 1\. El usuario accede a la sección de catálogo o venta. 2\. Busca el producto deseado. 3\. Selecciona la opción “Agregar al carrito”. 4\. El sistema agrega el producto al carrito con su cantidad y precio. 5\. Se actualiza visualmente el carrito.  |
| **Postcondición** | El producto queda registrado en el carrito del usuario |
| **Excepción** | Si el producto no existe, o existe un problema con el stock del producto, entonces un mensaje de error es desplegado. |

4. ### ESTRUCTURAR MODELO DE CASOS DE USO {#estructurar-modelo-de-casos-de-uso}

   2. ## **Flujo de Trabajo: Análisis**  {#flujo-de-trabajo:-análisis}

      1. ### ANÁLISIS DE ARQUITECTURA {#análisis-de-arquitectura}

      2. ### ANÁLISIS DE CASOS DE USO {#análisis-de-casos-de-uso}

      3. ### ANÁLISIS DE CLASE {#análisis-de-clase}

      4. ### ANÁLISIS DE PAQUETE {#análisis-de-paquete}

   3. ## **Flujo de Trabajo: Diseño** {#flujo-de-trabajo:-diseño}

      1. ### DISEÑO DE ARQUITECTURA {#diseño-de-arquitectura}

         1. #### DIAGRAMA DESPLIEGUE {#diagrama-despliegue}

         2. #### DIAGRAMA ORGANIZADO EN CAPAS {#diagrama-organizado-en-capas}

      2. ### DISENO CASOS DE USO {#diseno-casos-de-uso}

      3. ### DISENO DE DATOS {#diseno-de-datos}

      4. ### DIAGRAMA DE CLASES {#diagrama-de-clases}

   4. ## **Flujo de Trabajo: Implementación** {#flujo-de-trabajo:-implementación}

      1. ### ELECCIÓN DE PLATAFORMA DE DESARROLLO DE SOFTWARE {#elección-de-plataforma-de-desarrollo-de-software}

      2. ### IMPLEMENTACIÓN ARQUITECTURA DEL SISTEMA  {#implementación-arquitectura-del-sistema}

   5. ## **Flujo de Trabajo: Pruebas**  {#flujo-de-trabajo:-pruebas}

## **CONCLUSIÓN**  {#conclusión}

## **RECOMENDACIÓN**  {#recomendación}

## **BIBLIOGRAFÍA**  {#bibliografía}