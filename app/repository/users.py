from sqlalchemy.orm import Session

from app.models import User

def get_user(db: Session, login: str) -> User | None: 
    return db.query(User).filter(User.login == login).scalar()

def create_user(db: Session, login: str, hashed_password: str) -> User:
    user = User(login=login, hashed_password=hashed_password)
    db.add(user)
    db.flush()
    return user