import os

from utils.jwt import get_user_id_from_token

from app.models import Document, Pet
from database import db

FILE_STORAGE_PATH = os.environ.get("FILE_STORAGE_PATH")


def get_documents_for_pet(pet_id, jwt_token):
    pet = Pet.query.get(pet_id)
    jwt_user_id = get_user_id_from_token(jwt_token)
    if not pet:
        return {"error": "Pet not found"}, 404
    if pet.owner_id != jwt_user_id:
        return {"error": "You are not authorized to view this pet's documents"}, 403

    documents = Document.query.filter_by(pet_id=pet_id).all()
    if documents:
        return [document.to_dict() for document in documents], 200
    else:
        return {"error": "No documents found for this pet"}, 404


def add_document_for_pet(data, jwt_token):
    pet_id = data.get("pet_id")
    pet = Pet.query.get(pet_id)
    jwt_user_id = get_user_id_from_token(jwt_token)
    if not pet:
        return {"error": "Pet not found"}, 404
    if pet.owner_id != jwt_user_id:
        return {"error": "You are not authorized to view this pet's documents"}, 403

    owner_id = pet.owner_id
    file = data.get("file")
    file_path = f"{FILE_STORAGE_PATH}/{file.filename}"
    file.save(file_path)

    new_document = Document(
        pet_id=pet_id, owner_id=owner_id, file_path=file_path, file_name=file.filename
    )
    db.session.add(new_document)
    db.session.commit()
    return {"message": "Document added successfully"}, 201


def delete_document(pet_id, document_id, jwt_token):
    pet = Pet.query.get(pet_id)
    jwt_user_id = get_user_id_from_token(jwt_token)
    if not pet:
        return {"error": "Pet not found"}, 404
    if pet.owner_id != jwt_user_id:
        return {"error": "You are not authorized to view this pet's documents"}, 403

    document = Document.query.filter_by(id=document_id, pet_id=pet_id).first()
    if document:
        db.session.delete(document)
        db.session.commit()
        return {"message": "Document deleted successfully"}, 200
    else:
        return {"error": "Document not found"}, 404
