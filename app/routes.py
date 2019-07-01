# -*- coding: utf-8 -*-
import os, datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request, send_from_directory,render_template_string
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.models import User, UserRoles, Role


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/users_table')
@roles_required('Admin')
def users_table():
    users = User.query.filter(User.username != current_user.username)
    return render_template('table.html', users=users)

@app.route('/role/<user>')
@roles_required('Admin')
def roles_form(user):
    user = User.query.filter(User.username == user).first()
    roles = Role.query.all()
    return render_template('user_roles.html', user=user, roles=roles)

@app.route('/delete_role/<user>/<role>')
@roles_required('Admin')
def delete_role(user, role):
    db_user = User.query.filter(User.username == user).first()
    db_user.delete_role(role)
    return redirect(url_for('roles_form', user=user))

@app.route('/append_role/<user>/<role>')
@roles_required('Admin')
def append_role(user, role):
    db_user = User.query.filter(User.username == user).first()
    db_user.append_role(role)
    return redirect(url_for('roles_form', user=user))


@app.route('/members')
@login_required    # Use of @login_required decorator
def member_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Members page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>{%trans%}Member Page{%endtrans%}</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('admin_page') }}>{%trans%}Admin Page{%endtrans%}</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    # The Admin page requires an 'Admin' role.
@app.route('/product_form')
def product_form():
    return render_template('product_form.html')
@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Admin Page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>{%trans%}Member Page{%endtrans%}</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('admin_page') }}>{%trans%}Admin Page{%endtrans%}</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)