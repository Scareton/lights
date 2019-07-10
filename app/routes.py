# -*- coding: utf-8 -*-
import os, datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request, send_from_directory,render_template_string
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.models import User, UserRoles, Role, Product, Component, Specification, ModalComponent
from app.forms import ProductForm, ComponentForm, SpecificationForm


@app.route('/')
@login_required
def home_page():
    return render_template('index.html')

@app.route('/search')
@login_required
def search():
    components = Component.query.all()
    return render_template('search_component.html', components=components)

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


@app.route('/product_table')
@login_required
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
                return redirect(url_for('product_specification', product = product.id, det = 'hollow'))
    return render_template('create_product.html', form=form)

@app.route('/product_specification/<product>/<det>', methods = ['GET', 'POST'])
@login_required
def product_specification(product, det):
    modal = ModalComponent.query.first()
    form = SpecificationForm()
    if det == 'hollow':
        component_name = det
    else:
        component_name = Component.query.filter(Component.id==det).first().component_name
    components = Component.query.order_by(Component.component_name).all()
    if request.method == 'POST':
        if form.count.data is None:
            flash('Используйте "." вместо ","')
            return redirect(url_for('product_specification', modal=modal, product=product,component_name=component_name, components=components, specifications=Specification.query.filter(Specification.product_id==product) ))
        specification = Specification(form.component_type.data, product, det, form.count.data)
        db.session.add(specification)
        db.session.commit()
        return redirect(url_for('product_specification', modal=modal, component_name=component_name, det='hollow', product=product,components=components, specifications=Specification.query.filter(Specification.product_id==product)))
    return render_template('product_specification.html', modal=modal, component_name=component_name,det='hollow', form=form, components=components, specifications=Specification.query.filter(Specification.product_id==product), product=product)

@app.route('/component_table')
@login_required
def component_table():
    modal_component = ModalComponent.query.first()
    components = Component.query.all()[::-1]
    return render_template('component_table.html', components=components, modal_component=modal_component)

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
                return redirect(url_for('create_modal_component',  modal_component = component.id, det = 'hollow'))  
    return render_template('create_component.html', form=form)

@app.route('/product_info/<product>')
@login_required
def product_info(product):
    db_product = Product.query.filter(Product.id==product).first()
    specifications=Specification.query.filter(Specification.product_id==product)
    modal = ModalComponent.query.first()
    return render_template('product_info.html', product=db_product, modal=modal, specifications=specifications)

@app.route('/delete_component/<id>')
@login_required
def delete_component(id):
    Component.delete_component(id)
    return redirect(url_for('component_table'))  

@app.route('/delete_specification/<id>')
@login_required
def delete_specification(id):
    product = Specification.query.filter(Specification.id == id).first().product_id
    Specification.query.filter(Specification.id == id).delete()
    db.session.commit()
    return redirect(url_for('product_specification', product=product, det='hollow'))  

@app.route('/delete_product/<id>')
@login_required
def delete_product(id):
    Product.delete_product(id)
    return redirect(url_for('product_table'))  


@app.route('/create_modal_component/<modal_component>/<det>', methods = ['GET', 'POST'])
@login_required
def create_modal_component(modal_component, det):
    form = SpecificationForm()
    component_name = ''
    if det == 'hollow':
        component_name = det
    else:
        component_name = Component.query.filter(Component.id==det).first().component_name
    modals = db.session.query(ModalComponent.parrent_id).filter(ModalComponent.child_id==modal_component).all()
    components = Component.query.filter(Component.id!=modal_component).order_by(Component.component_name).all()
    if request.method == 'POST':
        if form.count.data is None:
            flash('Используйте "." вместо ","')
            return redirect(url_for('create_modal_component',modals=modals,  modal_component=modal_component,component_name=component_name, components=components, specifications=ModalComponent.query.filter(ModalComponent.parrent_id==modal_component) ))
        specification = ModalComponent( modal_component, det, form.count.data)
        db.session.add(specification)
        db.session.commit()
        return redirect(url_for('create_modal_component',modals=modals, modal_component=modal_component, det='hollow', component_name=component_name,components=components, specifications=ModalComponent.query.filter(ModalComponent.parrent_id==modal_component)))
    return render_template('create_modal_component.html',modals=modals, modal_component=modal_component,det='hollow',component_name=component_name, form=form, components=components, specifications=ModalComponent.query.filter(ModalComponent.parrent_id==modal_component))

@app.route('/delete_modal_component/<id>')
@login_required
def delete_modal_component(id):
    modal_component = ModalComponent.query.filter(ModalComponent.id == id).first().parrent_id
    ModalComponent.query.filter(ModalComponent.id == id).delete()
    db.session.commit()
    return redirect(url_for('create_modal_component', modal_component=modal_component, det='hollow')) 

@app.route('/component_info/<component>')
@login_required
def component_info(component):
    db_component = Component.query.filter(Component.id==component).first()
    specifications=ModalComponent.query.filter(ModalComponent.parrent_id==component)
    return render_template('component_info.html', component=db_component, specifications=specifications)