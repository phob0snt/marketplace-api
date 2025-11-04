from app.core.security import get_password_hash
from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate
from sqlalchemy.orm import Session


def create_account(user_data: AccountCreate, db: Session) -> AuthORM | None:
    new_user = AuthORM(
        login=user_data.login,
        password_hash=get_password_hash(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_account_by_id(manager_id: int, db: Session) -> AuthORM | None:
    manager = db.query(AuthORM).filter(AuthORM.id == manager_id).first()

    if not manager:
        return None

    return manager


def get_account_by_login(login: str, db: Session) -> AuthORM | None:
    return db.query(AuthORM).filter(AuthORM.login == login).first()
