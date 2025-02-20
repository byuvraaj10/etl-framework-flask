from flask import Blueprint, request, jsonify
from app.database_models import db, User

routes_bp = Blueprint("routes", __name__)

@routes_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "id": new_user.id}), 201

@routes_bp.route('/users', methods=['GET'])
def get_users():
    """Fetch all users"""
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users]), 200

@routes_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Fetch a single user by ID"""
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

@routes_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Update user details"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@routes_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Delete a user"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
