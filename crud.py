from sqlalchemy.orm import Session

import models

def get_number(db: Session, id: int):
    return db.query(models.Numbers).filter(models.Numbers.id == id).first()


def get_numbers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Numbers).offset(skip).limit(limit).all()