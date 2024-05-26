from database import db


class Owner(db.Model):
    __tablename__ = "owner"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(100))

    password = db.Column(db.String(300))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    pets = db.relationship("Pet", back_populates="owner")
    doctor = db.relationship("Doctor", back_populates="owners")

    appointments = db.relationship("Appointment", back_populates="owner")

    doctors_owners = db.Table(
        "doctors_owners",
        db.Column(
            "doctor_id", db.Integer, db.ForeignKey("doctor.id"), primary_key=True
        ),
        db.Column("owner_id", db.Integer, db.ForeignKey("owner.id"), primary_key=True),
    )

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Doctor(db.Model):
    __tablename__ = "doctor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(100))

    name = db.Column(db.String(100))

    password = db.Column(db.String(300))

    appointments = db.relationship("Appointment", back_populates="doctor")
    diagnostics = db.relationship("Diagnostic", back_populates="doctor")
    owners = db.relationship(
        "Owner",
        secondary=Owner.doctors_owners,
        back_populates="doctor",
    )

    def __init__(self, email=None, name=None, password=None):
        self.email = email
        self.password = password
        self.name = name

    def serialize(self):
        return {"id": self.id, "email": self.email, "name": self.name}
