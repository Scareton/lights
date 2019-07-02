# -*- coding: utf-8 -*-
import os, datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request, send_from_directory,render_template_string
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.models import User, UserRoles, Role, Product, Component, Specification
from app.forms import ProductForm, ComponentForm


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
@app.route('/product_table')
def product_table():
    products = Product.query.all()
    return render_template('product_table.html', products=products)

@app.route('/create_product', methods = ['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Не заполнены необходимые поля или введены некорректные данные')
            return render_template('create_product.html', form = form)
        else:
            if Product.query.filter(Product.product_name == form.name.data).first() or Product.query.filter(Product.product_item == form.item.data).first():
                flash('Товар с таким именем или артикулом существует')
                return render_template('create_product.html', form = form)  
            else:
                product = Product(form.name.data, form.power.data, form.item.data, form.weight.data, form.materials.data)
                db.session.add(product)
                db.session.commit()
                return redirect(url_for('product_table'))
    return render_template('create_product.html', form=form)

@app.route('/component_table')
def component_table():
    components = Component.query.all()[::-1]
    return render_template('component_table.html', components=components)

@app.route('/create_component', methods = ['GET', 'POST'])
@login_required
def create_component():
    form = ComponentForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Не заполнены необходимые поля или введены некорректные данные')
            return render_template('create_component.html', form = form)
        else:
            if Component.query.filter(Component.component_name == form.name.data).first() or Component.query.filter(Component.component_item == form.item.data).first():
                flash('Товар с таким именем или артикулом существует')
                return render_template('create_component.html', form = form)  
            else:
                component = Component(form.name.data, form.unit.data, form.item.data)
                db.session.add(component)
                db.session.commit()
                return redirect(url_for('component_table'))  
    return render_template('create_component.html', form=form)

@app.route('/product_info')
def product_info():
    products = Product.query.all()[::-1]
    return render_template('product_info.html', products=products)

@app.route('/delete_component/<id>')
def delete_component(id):
    Component.query.filter(Component.id == id).delete()
    db.session.commit()
    return redirect(url_for('component_table'))  

@app.route('/delete_product/<id>')
def delete_product(id):
    Product.query.filter(Product.id == id).delete()
    db.session.commit()
    return redirect(url_for('product_table'))  