from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, UTC  # ✅ Use UTC instead of utcnow()

# Naming convention to avoid migration issues
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)

    # ✅ Store timezone-aware UTC datetimes
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),  
        nullable=False
    )


