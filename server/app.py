from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        message_list = [{'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at} for message in messages]
        return jsonify(message_list)

    elif request.method == 'POST':
        try:
            data = request.json
            new_message = Message(body=data.get('body'), username=data.get('username'))
            db.session.add(new_message)
            db.session.commit()
            return jsonify({'id': new_message.id, 'body': new_message.body, 'username': new_message.username, 'created_at': new_message.created_at}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating a new message: {e}")
            return jsonify({"error": "Failed to create a new message"}), 500

@app.route('/messages/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_message(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({"error": f"Message with ID {id} not found"}), 404

    if request.method == 'GET':
        return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at})

    elif request.method == 'PUT':
        try:
            data = request.json
            message.body = data.get('body')
            message.username = data.get('username')
            db.session.commit()
            return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at})
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating message: {e}")
            return jsonify({"error": "Failed to update message"}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(message)
            db.session.commit()
            return jsonify({"message": "Message deleted successfully"})
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting message: {e}")
            return jsonify({"error": "Failed to delete message"}), 500

if __name__ == '__main__':
    app.run(port=5555)
