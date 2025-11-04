from sqlalchemy.orm import Session
from app.models.auth import AuthORM
from app.core.security import get_password_hash
from app.core import settings
import logging

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    try:
        admin = db.query(AuthORM).filter(AuthORM.role == "admin").first()

        if not admin:
            logger.info("Создание администратора по умолчанию...")

            admin_user = AuthORM(
                login=getattr(settings, "ADMIN_LOGIN", "admin"),
                password_hash=get_password_hash(
                    getattr(settings, "ADMIN_PASSWORD", "admin123")
                ),
                role="admin",
            )

            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            logger.info(f"Администратор создан: {admin_user.login}")
            logger.info(f"Login: {admin_user.login}")
            logger.info(f"Password: {getattr(settings, 'ADMIN_PASSWORD', 'admin123')}")
            create_test_user(db)
        else:
            logger.info(f"Администратор уже существует: {admin.login}")

    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {str(e)}")
        db.rollback()
        raise


def create_test_user(
    db: Session, login: str = "test_user", password: str = "password123"
) -> AuthORM | None:
    try:
        existing_user = db.query(AuthORM).filter(AuthORM.login == login).first()

        if not existing_user:
            logger.info(f"Создание тестового пользователя: {login}")

            test_user = AuthORM(
                login=login, password_hash=get_password_hash(password), role="user"
            )

            db.add(test_user)
            db.commit()
            db.refresh(test_user)

            logger.info(f"Тестовый пользователь создан: {login}")
            return test_user
        else:
            logger.info(f"Пользователь {login} уже существует")
            return existing_user

    except Exception as e:
        logger.error(f"Ошибка при создании тестового пользователя: {str(e)}")
        db.rollback()
        return None
