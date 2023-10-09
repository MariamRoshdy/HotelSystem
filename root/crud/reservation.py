from sqlalchemy.orm import Session
from database.models import Reservation
from schemas.reservation import Reservation as Res


def add_reservation(db: Session, reservation: Res, user_id: int):
    db_reservation = Reservation(user_id=user_id,
                                 room_type=reservation.room_type,
                                 start_date=reservation.start_date,
                                 end_date=reservation.End_date)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db


def del_reservation(db: Session, reservation_id: int):
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    db.delete(reservation)
    db.commit()
    db.close()
    return db


def list_reservations(db: Session):
    return db.query(Reservation).all()
