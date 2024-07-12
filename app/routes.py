from flask import request, jsonify
from app import app, db
from app.models import Comment

@app.route('/api/comment/new', methods=['POST'])
def create_comment():
    data = request.get_json()
    new_comment = Comment(email=data['email'], comment=data['comment'], content_id=data['content_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully!'}), 201

@app.route('/api/comment/list/<int:content_id>', methods=['GET'])
def list_comments(content_id):
    comments = Comment.query.filter_by(content_id=content_id).all()
    result = [
        {'email': comment.email, 'comment': comment.comment} for comment in comments
    ]
    return jsonify(result), 200
