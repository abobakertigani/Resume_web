from flask_sqlalchemy import SQLAlchemy

# سنستخدم db ككائن مشترك بين الملفات
db = SQLAlchemy()

# موديل الكورس
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    registration_form = db.Column(db.String(200))

    def __repr__(self):
        return f'<Course {self.title}>'