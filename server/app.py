from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages')
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    # Convert messages to a list of dictionaries
    messages_list = [message.to_dict() for message in messages]
    # Return as JSON
    return jsonify(messages_list)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

# Add the POST route for creating messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    new_message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

# Add the PATCH route for updating messages
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)  # Updated line
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    data = request.get_json()
    
    if 'body' in data:
        message.body = data['body']
    
    db.session.commit()
    
    return jsonify(message.to_dict())

# Add the DELETE route for deleting messages
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)  # Updated line
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    db.session.delete(message)
    db.session.commit()
    
    return "", 204

if __name__ == '__main__':
    app.run(port=5555)
