from website import db

class LinkCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    stub = db.Column(db.String(128), unique=True)
    links = db.relationship('Link', backref="category", cascade="all, delete, delete-orphan")
    rank = db.Column(db.Integer, unique=True)

    def __str__(self):
        return self.name

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_text = db.Column(db.String(128))
    url = db.Column(db.String(512))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('link_category.id'))
    rank = db.Column(db.Integer, unique=True)

