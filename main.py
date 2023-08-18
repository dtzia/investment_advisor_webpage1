import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired
import datetime


app = Flask(__name__)

#CREATE USER DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
db = SQLAlchemy(app)

#CREATE TABLE for messages.db
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    message = db.Column(db.String(1000))

    def __init__(self, fullname, email, phone, message):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.message = message


#CREATE TABLE for submissions.db
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    question1 = db.Column(db.String(1000))
    question2 = db.Column(db.String(1000))
    question3 = db.Column(db.String(1000))
    question4 = db.Column(db.String(1000))
    question5 = db.Column(db.String(1000))
    question6 = db.Column(db.String(1000))
    question7 = db.Column(db.String(1000))
    question8 = db.Column(db.String(1000))

    def __init__(self, fullname, phone, email, question1, question2, question3, question4, question5, question6, question7, question8):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.question4 = question4
        self.question5 = question5
        self.question6 = question6
        self.question7 = question7
        self.question8 = question8


class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))

    def __init__(self, fullname, email):
        self.fullname = fullname
        self.email = email


with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')

class NewsletterForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('E-Mail Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')
class ContactForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('E-Mail Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class QuestionsForm(FlaskForm):
    not_member_name = StringField('Όνομα', validators=[DataRequired()])
    not_member_email = StringField('Email', validators=[DataRequired(), Email(check_deliverability=True)])
    not_member_phone = StringField('Τηλέφωνο επικοινωνίας', validators=[DataRequired()])
    question1 = SelectField(label='Ποιός λόγος σας οδηγεί στην ανάγκη συσσώρευσης κεφαλαίου;', choices=['Εξασφάλιση οικογένειας - Κάλυψη σπουδών', 'Εξασφάλιση Συμπληρωματικής Σύνταξης', 'Επένδυση διαθέσιμων κεφαλαίων & Προστασία εισοδήματος'], validators=[DataRequired()])
    question2 = SelectField(label='Σε πόσα χρόνια θεωρείτε οτι θα χρειαστείτε το κεφάλαιο που αποταμιεύετε και επενδύετε;', choices=['Σε χρονικό διάστημα που δεν ξεπερνά τα 3 έτη', 'Μετά από 3 έτη, αλλά όχι περισσότερα απο 6', 'Σε περισσότερα από 6 έτη αλλά όχι περισσότερα από 10', 'Μετά από 10 έτη, αλλά όχι παραπάνω από 15', 'Σε περισσότερα από 15 έτη'], validators=[DataRequired()])
    question3 = IntegerField(label="Με βάση την παραπάνω χρονική διάρκεια που επιλέξατε, τι κεφάλαιο θα θέλατε να συσσωρεύσετε στο πέρας του συγκεκριμένου χρονικού διαστήματος;", validators=[DataRequired()])
    question4 = SelectField('Ποιά από τις παρακάτω προτάσεις θεωρείτε οτι σας ταιριάζει καλύτερα;', choices=['Η διατήρηση του αρχικού μου κεφαλαίου είναι η βασικότερη επιδίωξή μου ακόμα και αν αυτό είναι σε βάρος της άυξησης του κεφαλαίου μου', 'Κάποιες διακυμάνσεις του κεφαλαίου μου είναι αποδεκτές, με αντάλλαγμα αυξημένες πιθανότητες για υψηλότερες αποδόσεις', 'Ενδιαφέρομαι μόνο για υψηλές αποδόσεις, ανεξάρτητα από τις πολύ μεγάλες διακυμάνσεις του κεφαλαίου μου'], validators=[DataRequired()])
    question5 = SelectField('Σε ποιές από τις παρακάτω κατηγορίες προϊόντων έχετε κυρίως τοποθετήσει χρήματα ή έχετε επενδύσει στο παρελθόν;', choices=['Σε τραπεζικές ή προθεσμιακές καταθέσεις', 'Αμοιβαία κεφάλαια διαχείρισης διαθεσίμων', 'Ομόλογα ή/και ομολογιακά αμοιβαία κεφάλαια', 'Μικτά αμοιβαία κεφάλαια', 'Συνταξιοδοτικά ασφαλιστικά προγράμματα', 'Μετοχές ή/και μετοχικά αμοιβαία κεφάλαια', 'Σύνθετα αμοιβαία κεφάλαια ή/και παράγωγα χρηματιστηριακά προϊόντα(futures, options κλπ)'], validators=[DataRequired()])
    question6 = SelectField('Η αξία των επενδύσεων σας μπορεί να αυξάνεται ή να μειώνεται. Πόση μείωση της συνολικής αξίας της επένδυσης σας θα σας έκανε να νιώθετε ιδιαίτερα δυσάρεστα;', choices=['Οποιαδήποτε μείωση θα με έκανε να νιώθω ανασφαλής', '10%', '20%', '33% ή και περισσότερο'], validators=[DataRequired()])
    question7 = SelectField('Έχετε γνώσεις σχετικά με επενδύσεις και χρηματοπιστωτικά προϊόντα όπως μετοχές, ομόλογα, αμοιβαία κεφάλαια,  και κατηγορίες τους, παράγωγα, διαχείριση επενδυτικού χαρτοφυλακίου, συνταξιοδοτικά ασφαλιστικά προγράμματα;', choices=['Δεν έχω καθόλου γνώσεις', 'Έχω λίγες γνώσεις', 'Έχω αρκετές γνώσεις', 'Γνωρίζω καλά και είμαι απόλυτα εξοικειωμένος με τις διάφορες κατηγορίες επενδυτικών προϊόντων'], validators=[DataRequired()])
    question8 = SelectField('Σε ποιά ηλικιακή κατηγορία ανήκετε;', choices=['18-30', '30-45', '45-55', '>55'], validators=[DataRequired()])
    submit = SubmitField('Submit')


def check_contact_form_validity(contact_form):
    if contact_form.validate_on_submit():
        fullname = contact_form.fullname.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        if not fullname or not phone or not email:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία')
            return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    check_contact_form_validity(contact_form)
    question_form = QuestionsForm()
    newsletter_form = NewsletterForm()
    current_year = datetime.datetime.now().year
    if question_form.validate_on_submit():
        name = question_form.not_member_name.data
        email = question_form.not_member_email.data
        phone = question_form.not_member_phone.data
        questions = [question_form['question' + str(i)].data for i in range(1, 9)]
        new_submission = Submission(fullname=name, email=email, phone=phone, question1=questions[0], question2=questions[1], question3=questions[2], question4=questions[3], question5=questions[4], question6=questions[5], question7=questions[6], question8=questions[7])
        db.session.add(new_submission)
        db.session.commit()
        flash('Thank you for your submission! We will contact you with your investment plan as soon as possible', category='question_success')

        return redirect(url_for('home', _anchor='question-section'))
    if contact_form.validate_on_submit():
        fullname = contact_form.fullname.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        new_message = Message(fullname=fullname, email=email, phone=phone, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you for your message! We will contact you as soon as possible', category='contact_success')

        return redirect(url_for('home', _anchor='contact-section'))
    if newsletter_form.validate_on_submit():
        fullname = newsletter_form.fullname.data
        email = newsletter_form.email.data
        new_member = Newsletter(fullname=fullname, email=email)
        db.session.add(new_member)
        db.session.commit()
        flash('Η εγγραφή σου ολοκληρώθηκε με επιτυχία!', category='subscription_success')

        return redirect(url_for('home', _anchor='newsletter-section'))

    return render_template('form.html', form=contact_form, question_form=question_form, newsletter_form=newsletter_form, current_year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
