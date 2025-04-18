from app.db.session import engine
from app.db.base import Base
from app.models import user  # Importá modelos para que SQLAlchemy los registre

def main():
    print("✅ Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas y actualizadas.")

main()
