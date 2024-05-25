from database import db


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"))

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))

    file_path = db.Column(db.String(100))

    date_created = db.Column(db.DateTime)

    def __init__(
        self,
        image=None,
        owner_id=None,
        date_created=None,
        file_path=None,
    ):
        self.image = image
        self.owner_id = owner_id
        self.date_created = date_created
        self.file_path = file_path

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
            "ownerId": self.owner_id,
            "dateCreated": self.date_created,
            "filePath": self.file_path,
        }
