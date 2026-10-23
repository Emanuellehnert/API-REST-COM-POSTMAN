from uuid import uuid4
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from db import db
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(String(100), nullable=False)
    author = db.Column(String(100), nullable=False)
    description = db.Column(Text, nullable=True)
    is_reading = db.Column(db.Boolean, nullable=False, default=False)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)
    is_favorite = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"<Book {self.title}>"
#transformando o objeto em dicionário
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "is_reading": self.is_reading,
            "is_finished": self.is_finished,
            "is_favorite": self.is_favorite
        }
    