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


class TreatmentPlan(db.Model):
    __tablename__ = "treatment_plan"

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))

    current_stage = db.Column(db.Integer)

    stages = db.relationship("TreatmentStage", back_populates="treatment_plan")

    def __init__(
        self,
        owner_id=None,
        date_created=None,
    ):
        self.owner_id = owner_id
        self.date_created = date_created
