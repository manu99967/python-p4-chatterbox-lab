from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    @app.route("/messages", methods=["GET"])
    def get_messages():
        messages = Message.query.all()
        return jsonify([{
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at.isoformat()
        } for m in messages])

    @app.route("/messages", methods=["POST"])
    def create_message():
        data = request.get_json()
        m = Message(body=data["body"], username=data["username"])
        db.session.add(m)
        db.session.commit()
        return jsonify({
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at.isoformat()
        }), 201

    @app.route("/messages/<int:id>", methods=["PATCH"])
    def update_message(id):
        data = request.get_json()
        m = Message.query.get_or_404(id)
        if "body" in data:
            m.body = data["body"]
        db.session.commit()
        return jsonify({
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at.isoformat()
        })

    @app.route("/messages/<int:id>", methods=["DELETE"])
    def delete_message(id):
        m = Message.query.get_or_404(id)
        db.session.delete(m)
        db.session.commit()
        return '', 204

    return app


# Only run if executed directly
if __name__ == "__main__":
    create_app().run(port=5555, debug=True)

