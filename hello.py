from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hBGQNMa7wlpWGxN8z5B0m0qNNQz8WfQe' # flask wtf

bootstrap = Bootstrap(app)
moment = Moment(app)


class MainForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))

    email_msg = None
    email = session.get('email')
    if email is not None:
        if "utoronto" in email:
            email_msg = 'Your UofT email is ' + email
        else:
            email_msg = 'Please use your UofT email.'

    return render_template('index.html', form=form,
        name=session.get('name'), email_msg=email_msg)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Not sure if this is required? it's part of Chapter 3
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
