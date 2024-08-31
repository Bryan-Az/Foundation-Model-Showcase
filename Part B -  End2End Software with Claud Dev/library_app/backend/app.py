from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

books = [
    {"id": 1, "title": "The Great Georgia Gatsby", "content": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. 'Whenever you feel like criticizing any one,' he told me, 'just remember that all the people in this world haven't had the advantages that you've had.'"},
    {"id": 2, "title": "To Save a Penguin", "content": "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. Even after it healed, he couldn't fully extend it, and it caused him great frustration. But despite the setback, Jem never let it stop him from pursuing his dreams. He became an advocate for penguin conservation, dedicating his life to saving these incredible creatures from extinction."},
    {"id": 3, "title": "1999", "content": "It was a bright cold day in April, and the clocks were striking thirteen. The world was on the brink of a new millennium, filled with uncertainty and anticipation. People wondered what the future would hold, what technological advancements would shape our lives, and how society would evolve. Little did they know that the year 1999 would be a turning point in history, marking the beginning of a new era."},
]

# Simple user credential 'database'
users = {
    "admin": "password123"
}

@app.route('/api/books')
def get_books():
    return jsonify(books)

@app.route('/api/books/<int:book_id>')
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)