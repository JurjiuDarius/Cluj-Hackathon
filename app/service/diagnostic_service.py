from app.models import Diagnostic
from database import db


def create_diagnostic(data):
    text = data["text"]
    image_id = data["image_id"]
    doctor_id = data["doctor_id"]

    diagnostic = Diagnostic(text=text, image_id=image_id, doctor_id=doctor_id)

    db.session.add(diagnostic)
    db.session.commit()

    return diagnostic.serialize(), 201


def get_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.query.get(diagnostic_id)
    return diagnostic.serialize(), 200


def get_diagnostic_for_image(image_id):
    diagnostic = Diagnostic.query.filter_by(image_id=image_id).first()
    if not diagnostic:
        diagnostic = Diagnostic(text="No diagnostic yet")
    return diagnostic.serialize(), 200


def update_diagnostic(updated_data):
    if "id" in updated_data and updated_data["id"] is not None:
        diagnostic_id = updated_data["id"]
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if diagnostic:
            diagnostic.text = updated_data["text"]
            db.session.commit()
            return diagnostic.serialize(), 200
        return {"message": "Diagnostic not found"}, 404

    doctor_id = updated_data["doctorId"]
    image_id = updated_data["imageUploadId"]
    text = updated_data["text"]
    diagnostic = Diagnostic(doctor_id=doctor_id, image_id=image_id, text=text)
    db.session.add(diagnostic)
    db.session.commit()
    return diagnostic.serialize(), 201


def delete_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.query.get(diagnostic_id)
    if not diagnostic:
        return {"message": "Diagnostic not found"}, 404
    db.session.delete(diagnostic)
    db.session.commit()
    return {"message": "Diagnostic deleted successfully"}, 200
