"""first app is package name"""
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests

from config import Config
from app.access_token import AccessToken
from app import db
from app.models import User

from app.auth.forms import *
from app.auth.email import send_password_reset_mail
from app.auth import bp

"""
When a user that is not logged in accesses a view function protected with the 
@login_required decorator, the decorator is going to redirect to the login page, 
but it is going to include some extra information in this redirect so that the 
application can then return to the first page. If the user navigates to /index, 
for example, the @login_required decorator will intercept the request and 
respond with a redirect to /login, but it will add a query string argument to 
this URL, making the complete redirect URL /login?next=/index. The next query 
string argument is set to the original URL, so the application can use that to 
redirect back after login.
"""
@bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('login called')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        api_url = Config.API_ROOT + "/api/login_user"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        data = { 
            'user_id': user.id
        }
        response = requests.post(api_url, json=data, headers=headers)
        print(response.json())
        if response.json()['status'] != 0:
            flash(response.json()['result'])
            return redirect(url_for('auth.login'))
                            
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    current_app.logger.info('logout called')
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    print("register")
    current_app.logger.info('register called')
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            print("register1")

            api_url = Config.API_ROOT + "/api/create_user"
            token = AccessToken().get_access_token()
            headers = {'Authorization': "Bearer {}".format(token)}
            data = { 
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
            response = requests.post(api_url, json=data, headers=headers)
            print(response.json())
            if response.json()['status'] == 0:
                flash('Registered!')
            else:
                flash('Registered without Remote Synch!') # need to deal with this case
            print("register2")

        except Exception as error:
            db.session.rollback()
            flash(f'Failed to register! Error={error}')

    return render_template('register.html', title='Register', form=form)
        
@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    current_app.logger.info('reset_password_request called')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            api_url = Config.API_ROOT + "/api/send_password_reset_mail"
            token = AccessToken().get_access_token()
            headers = {'Authorization': "Bearer {}".format(token)}
            data = { 
                'user_id': user.id
            }
            response = requests.post(api_url, json=data, headers=headers)
            if response.json()['status'] == 0:
                flash('Check your email for the instructions to reset your password')
            else:
                flash('Could not send email. Please retry.')
                return render_template('reset_password_request.html', title='Reset Password', form=form)
        else:
            flash('Can not match email with a valid user.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password_request.html', title='Reset Password', form=form)
        
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    current_app.logger.info('reset_password called')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    api_url = Config.API_ROOT + "/api/verify_reset_password_token"
    token = AccessToken().get_access_token()
    headers = {'Authorization': "Bearer {}".format(token)}
    data = { 
        'token': token
    }
    response = requests.post(api_url, json=data, headers=headers)
    user_id = int(response.json()['user_id'])
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('main.index'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    current_app.logger.info('change_password called')
        
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.old_password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.change_password'))
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed')
        return redirect(url_for('auth.login'))
    return render_template('change_password.html', form=form)
    
@bp.route('/user_list', methods=['GET'])
@login_required
def user_list():
    current_app.logger.info('GET user_list called')
    users = User().query.all()
    
    return render_template('user_list.html', users=users)    
