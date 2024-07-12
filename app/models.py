from app import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Comment {self.email} - {self.content_id}>'
