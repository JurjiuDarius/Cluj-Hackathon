from database import db


class Pet(db.Model):
    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100))

    breed = db.Column(db.String(100))

    age = db.Column(db.Integer)

    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"))

    owner = db.relationship("Owner", back_populates="pets")

    diagnostics = db.relationship("Diagnostic", back_populates="pet")

    def __init__(self, name=None, breed=None, age=None, owner_id=None):
        self.name = name
        self.breed = breed
        self.owner_id = owner_id
        self.age = age

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "owner_id": self.owner_id,
        }
