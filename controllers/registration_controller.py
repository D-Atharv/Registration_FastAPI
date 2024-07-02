from sqlalchemy.orm import Session
from database.models import Registration, Event, Student
from schema.registrationSchema import RegistrationSchema


def get_all_registrations(db: Session):
    try:
        registrations = db.query(Registration).all()
        if not registrations:
            return {"error": "No registrations found"}
        return registrations
    except Exception as e:
        return {"error": str(e)}


def get_registration(registration_id: int, db: Session):
    try:
        registration = db.query(Registration).filter(Registration.uuid == registration_id).first()
        if not registration:
            return {"error": "Registration not found"}
        return registration
    except Exception as e:
        return {"error": str(e)}


def create_registration(registration: RegistrationSchema, db: Session):
    try:
        # Check if the event exists
        event = db.query(Event).filter(Event.uuid == registration.eventId).first()
        if not event:
            return {"error": "Event not found"}

        # Check if the student exists
        student = db.query(Student).filter(Student.uuid == registration.studentId).first()
        if not student:
            return {"error": "Student not found"}

        new_registration = Registration(eventId=registration.eventId, studentId=registration.studentId)
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        return new_registration
    except Exception as e:
        db.rollback()  # Rollback transaction on error to maintain consistency
        return {"error": str(e)}


def update_registration(registration_id: int, registration: RegistrationSchema, db: Session):
    try:
        selected_registration = db.query(Registration).filter(Registration.uuid == registration_id).first()

        if not selected_registration:
            return {"error": "Registration not found"}

        if registration.eventId is not None:
            # Check if the event exists
            event = db.query(Event).filter(Event.uuid == registration.eventId).first()
            if not event:
                return {"error": "Event not found"}
            selected_registration.eventId = registration.eventId

        if registration.studentId is not None:
            # Check if the student exists
            student = db.query(Student).filter(Student.uuid == registration.studentId).first()
            if not student:
                return {"error": "Student not found"}
            selected_registration.studentId = registration.studentId

        db.commit()
        db.refresh(selected_registration)
        return selected_registration
    except Exception as e:
        db.rollback()  # Rollback transaction on error to maintain consistency
        return {"error": str(e)}


def delete_registration(registration_id: int, db: Session):
    try:
        registration = db.query(Registration).filter(Registration.uuid == registration_id).first()
        if not registration:
            return {"error": "Registration not found"}

        db.delete(registration)
        db.commit()
        return registration
    except Exception as e:
        db.rollback()  # Rollback transaction on error to maintain consistency
        return {"error": str(e)}
