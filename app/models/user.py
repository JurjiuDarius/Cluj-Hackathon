from database import db


class Owner(db.Model):
    __tablename__ = "owner"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(100))

    password = db.Column(db.String(300))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    pets = db.relationship("Pet", back_populates="owner")
    doctor = db.relationship("Doctor", back_populates="owners")

    doctors_owners = db.Table(
        "doctors_owners",
        db.Column(
            "doctor_id", db.Integer, db.ForeignKey("doctor.id"), primary_key=True
        ),
        db.Column("owner_id", db.Integer, db.ForeignKey("owner.id"), primary_key=True),
    )

    def __init__(self, email=None, password=None):
        super().__init__(email)
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

    password = db.Column(db.String(300))

    diagnostics = db.relationship("Diagnostic", back_populates="doctor")
    owners = db.relationship(
        "Owner",
        secondary=Owner.doctors_owners,
        back_populates="doctor",
    )

    def __init__(self, email=None, password=None):
        super().__init__(email)
        self.email = email
        self.password = password

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
