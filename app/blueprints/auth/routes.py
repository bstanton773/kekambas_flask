from . import bp as auth 
from app import db, mail, Message
from flask import render_template, request, flash, redirect, url_for, jsonify
from .forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


@auth.route('/register', methods=['GET', 'POST'])
def register():
    title = "Kekambas Blog | REGISTER"
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(username, email, password)
        
        # create a new instance of User
        new_user = User(username, email, password)
        # add new instance to our database
        db.session.add(new_user)
        # commit database
        db.session.commit()

        # Send email to new user
        msg = Message(f'Welcome, {username}', [email])
        msg.body = "Thank you for signing up for the Kekambas blog. I hope you enjoy our app!"
        msg.html = "<p>Thank you so much for signing up for the Kekambas blog. I hope you enjoy our app!</p>"

        mail.send(msg)

        flash("You have succesfully signed up!", "success")
        return redirect(url_for('index'))
    return render_template('register.html', title=title, form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = "Kekambas Blog | LOGIN"
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Email/Password. Please try again", 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        next_page = request.args.get('next')
        if next_page:
            return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('index'))

    return render_template('login.html', title=title, form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash("You have succesfully logged out", 'primary')
    return redirect(url_for('index'))


@auth.route('/myinfo')
@login_required
def myinfo():
    title = "Kekambas Blog | MY INFO"
    return render_template('my_info.html', title=title)
