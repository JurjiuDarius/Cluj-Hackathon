import datetime

from sqlalchemy import DateTime

from database import db


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"))

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))

    file_path = db.Column(db.String(100))

    file_name = db.Column(db.String(100))

    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self,
        owner_id=None,
        pet_id=None,
        date_created=None,
        file_path=None,
        file_name=None,
    ):
        self.owner_id = owner_id
        self.pet_id = pet_id
        self.date_created = date_created
        self.file_path = file_path
        self.file_name = file_name

    def serialize(self):
        return {
            "id": self.id,
            "ownerId": self.owner_id,
            "petId": self.pet_id,
            "dateCreated": self.date_created,
            "filePath": self.file_path,
        }
