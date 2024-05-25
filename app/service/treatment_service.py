from app.models import Treatment
from database import db


def create_treatment(data):
    text = data["text"]
    image_id = data["image_id"]
    doctor_id = data["doctor_id"]

    treatment = Treatment(text=text, image_id=image_id, doctor_id=doctor_id)

    db.session.add(treatment)
    db.session.commit()

    return treatment.serialize(), 201


def get_treatment(treatment_id):
    treatment = Treatment.query.get(treatment_id)
    return treatment.serialize(), 200


def update_treatment(updated_data):
    if "id" in updated_data and updated_data["id"] is not None:
        treatment_id = updated_data["id"]
        treatment = Treatment.query.get(treatment_id)
        if treatment:
            treatment.text = updated_data["text"]
            db.session.commit()
            return treatment.serialize(), 200
        return {"message": "Treatment not found"}, 404

    doctor_id = updated_data["doctorId"]
    pet_id = updated_data["imageUploadId"]
    current_stage = updated_data["currentStage"]
    diagnostic = updated_data["diagnostic"]

    treatment.doctor_id = doctor_id
    treatment.pet_id = pet_id
    treatment.current_stage = current_stage
    treatment.diagnostic = diagnostic

    db.session.commit()
    return treatment.serialize(), 201


def delete_treatment(treatment_id):
    treatment = Treatment.query.get(treatment_id)
    if not treatment:
        return {"message": "Treatment not found"}, 404
    db.session.delete(treatment)
    db.session.commit()
    return {"message": "Treatment deleted successfully"}, 200


def add_treatment_stage(data):
    treatment_id = data.get("treatment_id")
    stage = data.get("stage")
    treatment = Treatment.query.get(treatment_id)
    if not treatment:
        return {"message": "Treatment not found"}, 404
    treatment.stages.append(stage)
    db.session.commit()
    return {"message": "Stage added successfully"}, 200


def delete_treatment_stage(treatment_id, stage_number):
    treatment = Treatment.query.get(treatment_id)
    if not treatment or len(treatment.stages) < stage_number:
        return {"message": "Treatment or stage not found"}, 404
    treatment.stages.pop(stage_number - 1)
    db.session.commit()
    return {"message": "Stage deleted successfully"}, 200


def complete_treatment_stage(treatment_id, stage_number):
    treatment = Treatment.query.get(treatment_id)
    if not treatment or len(treatment.stages) < stage_number:
        return {"message": "Treatment or stage not found"}, 404
    treatment.stages[stage_number - 1].completed = True
    db.session.commit()
    return {"message": "Stage marked as completed"}, 200
