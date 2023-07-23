import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired

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

    def __init__(self, fullname, phone, email, question1, question2, question3, question4, question5, question6, question7):
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


with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


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
    question2 = IntegerField(label='Ποια είναι η χρονική διάρκεια των επενδύσεών σας; Πόσο καιρό σχεδιάζετε να κρατήσετε τα κεφάλαιά σας επενδυμένα;')
    question3 = StringField('Ποια είναι η ανοχή σας στον κίνδυνο; Νιώθετε άνετα με την πιθανή αστάθεια και τις διακυμάνσεις στην αξία των επενδύσεών σας για κάποιο χρονικό διάστημα, ή προτιμάτε πιο σταθερές αποδόσεις;', validators=[DataRequired()])
    question4 = StringField('Έχετε επενδύσει σε αμοιβαία κεφάλαια ή άλλα επενδυτικά μέσα στο παρελθόν(πχ. Ακίνητα); Αν ναι, ποιους τύπους επενδύσεων είχατε και πώς απέδοσαν;', validators=[DataRequired()])
    question5 = StringField('Είστε εξοικειωμένος με την έννοια της διαφοροποίησης; Κατανοείτε τη σημασία της κατανομής των επενδύσεών σας σε διάφορα είδη περιουσιακών στοιχείων για τη διαχείριση του κινδύνου;', validators=[DataRequired()])
    question6 = StringField('Έχετε κάποιες συγκεκριμένες επενδυτικές προτιμήσεις ή πεποιθήσεις; Για παράδειγμα, ενδιαφέρεστε για επενδύσεις φιλικές προς το περιβάλλον ή έχετε κάποιο συγκεκριμένο κλάδο ή βιομηχανία στην οποία θα θέλατε να επικεντρωθείτε;', validators=[DataRequired()])
    question7 = StringField('Ποιά είναι η τρέχουσα οικονομική σας κατάσταση; Είστε σε θέση να αντέξετε πιθανές απώλειες για κάποιο μικρό χρονικό διάστημα, ή χρειάζεστε πιο σταθερές αποδόσεις για να επιτύχετε τους οικονομικούς σας στόχους;', validators=[DataRequired()])
    submit = SubmitField('Submit')


def check_contact_form_validity(contact_form):
    if contact_form.validate_on_submit():
        fullname = contact_form.fullname.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        if not fullname or not phone or not email:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία', 'error')
            return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    check_contact_form_validity(contact_form)
    question_form = QuestionsForm()
    if question_form.validate_on_submit():
        name = question_form.not_member_name.data
        email = question_form.not_member_email.data
        phone = question_form.not_member_phone.data
        questions = [question_form['question' + str(i)].data for i in range(1, 8)]
        new_submission = Submission(fullname=name, email=email, phone=phone, question1=questions[0], question2=questions[1], question3=questions[2], question4=questions[3], question5=questions[4], question6=questions[5], question7=questions[6])
        db.session.add(new_submission)
        db.session.commit()
        flash('Thank you for your submission! We will contact you with your investment plan as soon as possible', 'success')
        return redirect(url_for('home'))
    if contact_form.validate_on_submit():
        fullname = contact_form.fullname.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        new_message = Message(fullname=fullname, email=email, phone=phone, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you for your message! We will contact you as soon as possible', 'success')

        return redirect(url_for('home'))

    return render_template('form.html', form=contact_form, question_form=question_form)


if __name__ == "__main__":
    app.run(debug=True)
