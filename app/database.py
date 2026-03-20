from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app import models 
    
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Перевіряємо, чи таблиця юзерів порожня
        if db.query(models.User).count() == 0:
            # 1. Створюємо користувачів
            admin = models.User(username="admin1", password="Admin_1234567890", role="admin")
            user1 = models.User(username="user1", password="User_1234567890", role="user")
            
            db.add(admin)
            db.add(user1)

            db.commit() 
            
            test_password = models.PasswordItem(
                password_text="MySecret_2026!", 
                user_id=user1.id 
            )
            
            db.add(test_password)
            db.commit()
            
            print("Базу даних створено. Додано користувачів та тестовий пароль у таблицю passwords.")
    finally:
        db.close()