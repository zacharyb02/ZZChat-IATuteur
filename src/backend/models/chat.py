from datetime import datetime
from extensions import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="New Chat")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    messages = db.relationship(
        "Message",
        backref="chat",
        lazy=True,
        cascade="all, delete"
    )
