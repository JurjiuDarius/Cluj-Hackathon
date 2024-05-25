from database import db

from ..models.diagnostic import Appointment


def get_all_appointments_for_owner(owner_id):
    return [
        appointment.serialize()
        for appointment in Appointment.query.where(
            Appointment.owner_id == owner_id
        ).all()
    ], 200


def get_all_appointments_for_doctor(doctor_id):
    return [
        appointment.serialize()
        for appointment in Appointment.query.where(
            Appointment.doctor_id == doctor_id
        ).all()
    ], 200


def get_appointment_by_id(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return {"message": "Appointment not found!"}, 404
    return appointment.serialize(), 200


def create_appointment(data):
    try:
        if data["endTime"] < data["startTime"]:
            return {"message": "End time must be after start time"}, 400
        if data["endTime"] > "24:00:00" or data["startTime"] > "24:00:00":
            return {"message": "Time must be less than 24 hours"}, 400

        if "requirements" not in data:
            data["requirements"] = ""
        appointment = Appointment(
            requirements=data["requirements"],
            address=data["address"],
            date=data["date"],
            start_time=data["startTime"],
            end_time=data["endTime"],
            owner_id=data["ownerId"],
            doctor_id=data["doctorId"],
            requires_upload=data["requiresUpload"],
        )
        db.session.add(appointment)
        db.session.commit()
    except Exception:
        return {"message": "Invalid data"}, 400
    return appointment.serialize(), 201


def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    db.session.delete(appointment)
    db.session.commit()

def update_appointment(id, data):
    try:
        if data["endTime"] < data["startTime"]:
            return {"message": "End time must be after start time"}, 400
        # Check that none of the times are above 24 hours
        if data["endTime"] > "24:00:00" or data["startTime"] > "24:00:00":
            return {"message": "Time must be less than 24 hours"}, 400
        appointment = Appointment.query.get(id)
        appointment.requirements = data["requirements"]
        appointment.address = data["address"]
        appointment.date = data["date"]
        appointment.start_time = data["startTime"]
        appointment.end_time = data["endTime"]
        appointment.owner_id = data["ownerId"]
        appointment.doctor_id = data["doctorId"]
        appointment.requires_upload = data["requiresUpload"]
        db.session.commit()
    except Exception:
        return {"message": "Invalid data"}, 400
    return appointment.serialize(), 200
