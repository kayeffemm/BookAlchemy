from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author id={self.id} name={self.name} birth_date={self.birth_date} date_of_death={self.date_of_death}>"

    def __str__(self):
        return f"Author: {self.name}, born on {self.birth_date}, died on {self.date_of_death or 'N/A'}"


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"<Book id={self.id} isbn={self.isbn} title={self.title} publication_year={self.publication_year} author_id={self.author_id}>"

    def __str__(self):
        return f"Book: {self.title} (ISBN: {self.isbn}), published in {self.publication_year}"
