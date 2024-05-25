import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.json import json_serial_date
from database import db


class TreatmentStage(db.Model):
    __tablename__ = "treatment_stage"

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    stage_number = db.Column(db.Integer)

    treatment_plan_id = db.Column(db.Integer, db.ForeignKey("treatment_plan.id"))

    treatment_plan = db.relationship("TreatmentPlan", back_populates="stages")

    completed = db.Column(db.Boolean)

    description = db.Column(db.String(100))

    def __init__(
        self,
        treatment_plan_id=None,
        date_created=None,
        date_updated=None,
        description=None,
    ):
        self.treatment_plan_id = treatment_plan_id
        self.date_created = date_created
        self.date_updated = date_updated
        self.description = description

    def serialize(self):
        return {
            "id": self.id,
            "stageNumber": self.stage_number,
            "treatmentPlanId": self.treatment_plan_id,
            "completed": self.completed,
            "description": self.description,
        }


class TreatmentPlan(db.Model):
    __tablename__ = "treatment_plan"

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))

    diagnostic = db.Column(db.String(1000))

    current_stage = db.Column(db.Integer)

    start_date = db.Column(db.DateTime)

    end_date = db.Column(db.DateTime)

    stages = db.relationship("TreatmentStage", back_populates="treatment_plan")

    def __init__(
        self,
        owner_id=None,
        start_date=None,
        end_date=None,
        diagnostic=None,
        pet_id=None,
    ):
        self.owner_id = owner_id
        self.start_date = start_date
        self.end_date = end_date
        self.diagnostic = diagnostic
        self.pet_id = pet_id

    def serialize(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "pet_id": self.pet_id,
            "diagnostic": self.diagnostic,
            "startDate": json_serial_date(self.start_date),
            "endDate": json_serial_date(self.end_date),
            "currentStage": self.current_stage,
            "stages": [stage.serialize() for stage in self.stages],
        }
