from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import forms
import models

app = Flask(__name__)
app.secret_key = '234LWKJEr209U)(@r029fjpJ@)euf2fp2ej'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    # connect to the database
    g.db = models.database
    g.db.connect()


@app.after_request
def after_request(response):
    # close the db connection
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.select().where(
                models.User.email**form.email.data
            ).get()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You're now logged in!")
                return redirect(url_for('index'))
            else:
                flash("Email or password is invalid")
        except models.DoesNotExist:
            flash("Email or password is invalid")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out','success')
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('You are registered!','success')
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/taco',methods=['GET','POST'])
@login_required
def taco():
    form = forms.TacoForm()
    if request.method == 'POST':
        models.Taco.create(
            user=current_user._get_current_object(),
            protein=form.protein.data,
            shell=form.shell.data,
            cheese=form.cheese.data,
            extras=form.extras.data
        )
        flash('Taco created!','success')
        return redirect(url_for('index'))
    return render_template('taco.html',form=form)


@app.route('/')
def index():
    tacos = models.Taco.select().limit(15)
    return render_template('index.html', tacos=tacos)


if __name__ == "__main__":
    models.initialize()