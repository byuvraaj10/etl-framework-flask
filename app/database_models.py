from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  

    def __repr__(self):
        return f"<User {self.id}: {self.name} ({self.email})>"

    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by email"""
        return User.query.filter_by(email=email).first()
