import base64
import datetime

from sqlalchemy import Date, DateTime, Time

from app.utils.json import json_serial_date
from database import db


class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    requirements = db.Column(db.String(1000))

    address = db.Column(db.String(200))

    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"))

    owner = db.relationship("Owner", back_populates="appointments")

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    doctor = db.relationship("Doctor", back_populates="appointments")

    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)

    date = db.Column(Date)

    start_time = db.Column(Time)

    end_time = db.Column(Time)

    requires_upload = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        address=None,
        requirements=None,
        owner_id=None,
        doctor_id=None,
        date=None,
        requires_upload=None,
        start_time=None,
        end_time=None,
    ):
        self.address = address
        self.requirements = requirements
        self.owner_id = owner_id
        self.doctor_id = doctor_id
        self.date = date
        self.requires_upload = requires_upload
        self.start_time = start_time
        self.end_time = end_time

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "requirements": self.requirements,
            "ownerId": self.owner_id,
            "doctorId": self.doctor_id,
            "date": json_serial_date(self.date),
            "requiresUpload": self.requires_upload,
            "startTime": json_serial_date(self.start_time),
            "endTime": json_serial_date(self.end_time),
        }


class Diagnostic(db.Model):
    __tablename__ = "diagnostic"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    text = db.Column(db.String(1000))

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))
    pet = db.relationship("Pet", back_populates="diagnostics")

    doctor = db.relationship("Doctor", back_populates="diagnostics")

    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, doctor_id=None, text=None, image_id=None, date_created=None):
        self.text = text
        self.doctor_id = doctor_id
        self.date_created = date_created
        self.image_id = image_id

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "doctorId": self.doctor_id,
            "dateCreated": json_serial_date(self.date_created),
            "imageId": self.image_id,
        }
