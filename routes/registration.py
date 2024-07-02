from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import Registration, Event, Student
from schema.registrationSchema import RegistrationSchema

registrationRouter = APIRouter()

# GET route to get all registrations
@registrationRouter.get("/", response_model=dict)
async def get_registrations(db: Session = Depends(get_db)):
    try:
        registrations = db.query(Registration).all()
        if not registrations:
            return {"success": True, "message": "No registrations found"}
        return {"success": True, "data": registrations}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# GET route to get a specific registration
@registrationRouter.get("/{registration_id}", response_model=dict)
async def get_registration(registration_id: int, db: Session = Depends(get_db)):
    try:
        registration = db.query(Registration).filter(Registration.uuid == registration_id).first()
        if not registration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
        return {"success": True, "data": registration}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# POST route to create a new registration
@registrationRouter.post("/", response_model=dict)
async def create_registration(registration: RegistrationSchema, db: Session = Depends(get_db)):
    try:
        # Check if the event exists
        event = db.query(Event).filter(Event.uuid == registration.eventId).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # Check if the student exists
        student = db.query(Student).filter(Student.uuid == registration.studentId).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        new_registration = Registration(eventId=registration.eventId, studentId=registration.studentId)
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        return {"success": True, "data": new_registration}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# PUT route to update registration details
@registrationRouter.put("/{registration_id}", response_model=dict)
async def update_registration(registration_id: int, registration: RegistrationSchema, db: Session = Depends(get_db)):
    try:
        selected_registration = db.query(Registration).filter(Registration.uuid == registration_id).first()

        if not selected_registration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")

        if registration.eventId is not None:
            # Check if the event exists
            event = db.query(Event).filter(Event.uuid == registration.eventId).first()
            if not event:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
            selected_registration.eventId = registration.eventId

        if registration.studentId is not None:
            # Check if the student exists
            student = db.query(Student).filter(Student.uuid == registration.studentId).first()
            if not student:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
            selected_registration.studentId = registration.studentId

        db.commit()
        db.refresh(selected_registration)
        return {"success": True, "data": selected_registration}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# DELETE route to delete a registration
@registrationRouter.delete("/{registration_id}", response_model=dict)
async def delete_registration(registration_id: int, db: Session = Depends(get_db)):
    try:
        registration = db.query(Registration).filter(Registration.uuid == registration_id).first()
        if not registration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
        db.delete(registration)
        db.commit()
        return {"success": True, "data": registration}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
