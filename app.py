from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask.json import JSONEncoder
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# إعدادات البريد
SMTP_SERVER = "smtp.outlook.com"
SMTP_PORT = 587
SENDER_EMAIL = "Abusalih.adam@outlook.com"
SENDER_PASSWORD = "your-email-password"

# ---------------- دالة إرسال الإيميل ----------------
def send_email(user_name, user_email, user_message):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL
        msg['Subject'] = "📩 رسالة جديدة من نموذج الاتصال"

        body = f"""
        الاسم: {user_name}
        البريد الإلكتروني: {user_email}

        الرسالة:
        {user_message}
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())

        print("✅ تم إرسال الإيميل بنجاح")
    except Exception as e:
        print(f"❌ خطأ أثناء إرسال الإيميل: {e}")

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # ضروري لـ Flask-WTF
db = SQLAlchemy(app)

# ----------- الموديل (Model) -----------
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    registration_form = db.Column(db.String(200))

    def __repr__(self):
        return f'<Course {self.title}>'

# ----------- الفورم (Form) -----------
class CourseForm(FlaskForm):
    title = StringField('عنوان الكورس', validators=[DataRequired()])
    description = TextAreaField('وصف الكورس', validators=[DataRequired()])
    image_url = StringField('رابط الصورة', validators=[DataRequired(), URL()])
    registration_form = StringField('رابط استمارة التسجيل', validators=[DataRequired(), URL()])
    submit = SubmitField('إضافة كورس')

# ----------- الراوتات (Routes) -----------
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('AbuSalih.html', courses=courses)

@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            image_url=form.image_url.data,
            registration_form=form.registration_form.data
        )
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_course.html', form=form)

@app.route('/edit-course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.image_url = form.image_url.data
        course.registration_form = form.registration_form.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_course.html', form=form, course=course)

@app.route('/delete-course/<int:course_id>')
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('home'))



# الصفحة الرئيسية → واجهة الزائرين (AbuSalih.html)
@app.route('/')
def portfolio():
    courses = Course.query.all()  # جلب الكورسات من قاعدة البيانات
    return render_template('AbuSalih.html', courses=courses)

# ---------------- Route الاتصال ----------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_message = request.form['message']

        send_email(user_name, user_email, user_message)  # استدعاء الدالة هنا
        flash("✅ تم إرسال الرسالة بنجاح", "success")
        return redirect(url_for('portfolio'))

    return render_template('contact.html')

# بيانات الدخول (ممكن تعديلها لاحقاً لتكون من قاعدة البيانات)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash("تم تسجيل الدخول بنجاح ✅", "success")
            return redirect(url_for('manage_courses'))
        else:
            flash("❌ اسم المستخدم أو كلمة المرور غير صحيحة", "danger")

    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("تم تسجيل الخروج بنجاح ✅", "success")
    return redirect(url_for('portfolio'))

# حماية صفحة الإدارة
@app.route('/manage-courses')
def manage_courses():
    if not session.get('logged_in'):
        flash("⚠️ يجب تسجيل الدخول أولاً", "warning")
        return redirect(url_for('login'))

    courses = Course.query.all()
    return render_template('manage_courses.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
