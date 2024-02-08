from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import Clients
from db_func import add_client
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(6)], render_kw={"placeholder": "Пароль"})


class RegForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Имя"})
    email = EmailField("Email: ", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})


main = Blueprint('main', __name__)


@main.route('/')
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.admin_func_not_post'))
        else:
            return redirect(url_for('client.client_func'))
    form = LoginForm()
    return render_template('login.html', form=form)


@main.route('/', methods=['POST'])
def login_post():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    # здесь логика базы данных
    user = Clients.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Проверь правильность данных.')
        return redirect(url_for('main.login'))
    login_user(user, remember=True)
    if current_user.is_admin == 'True':
        return redirect(url_for('admin.admin_func'))
    return redirect(url_for('client.client_func'))


@main.route('/registration')
def registration():
    form = RegForm()
    return render_template('registration.html', form=form)


@main.route('/registration', methods=['POST'])
def registration_post():
    form = RegForm()
    email = form.email.data
    password = form.password.data
    name = form.name.data
    user = Clients.query.filter_by(
        email=email).first()
    if user:
        flash('Email уже зарегистрирован')
        return redirect(url_for('main.registration'))
    add_client([email, name, generate_password_hash(password)])
    return redirect(url_for('main.login'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


'''
          <form method="post" action="/change_prize">
            <button type="submit" class="knopka image-button" name="btn" value="{{i}} {{j}}"><img
                style="width: 30px; height: 30px; position: relative; right: 7px; bottom: 3px;"
                src="static/images/12345.svg"></button>
          </form>
          
          
          
          
                    <button class="image-button knopka_with_price" type="submit" name="update_prize" value="{{i}}"><img
                            class="image" src="static/prizes/{{sl_with_prizes[i][0]}}"></button>
                    <div class="nameprize"><b>{{sl_with_prizes[i][1]}}</b></div>
'''
