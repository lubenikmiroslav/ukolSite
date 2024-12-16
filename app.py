from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Regexp
from models import db, Person

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db.init_app(app)

# WTForm for adding a new person
class PersonForm(FlaskForm):
    id = FloatField('ID', validators=[DataRequired(), Regexp(r'^[0-9]+$', message="ID must be a number")])
    name = SelectField('Name', choices=[], validators=[DataRequired(), Regexp(r'^[ -~]+$', message="Name must contain only ASCII characters")])
    vyska = FloatField('Vyska (m)', validators=[DataRequired(), Regexp(r'^(\d{1,2}(\.\d{1,2})?|299(\.0{1,2})?)$', message="Vyska must be a valid number up to 299")])
    vaha = FloatField('Vaha (kg)', validators=[DataRequired(), Regexp(r'^(\d{1,2}(\.\d{1,2})?|199(\.0{1,2})?)$', message="Vaha must be a valid number up to 199")])
    submit = SubmitField('Add Person')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()
    if not Person.query.first():
        db.session.add_all([
            Person(name='Bertik', vyska=1.65, vaha=55),
            Person(name='Pepicek', vyska=1.80, vaha=75),
            Person(name='Anicka', vyska=1.75, vaha=85)
        ])
        db.session.commit()

@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    form.name.choices = [(person.name, person.name) for person in Person.query.all()]
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, vyska=form.vyska.data, vaha=form.vaha.data, id=form.id.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
