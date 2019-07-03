from app import db
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    def delete_role(self, del_role):
        for role in self.roles:
            self.roles.remove(Role.query.filter(Role.name==del_role).first())
            db.session.commit()
    def append_role(self, del_role):
            self.roles.append(Role.query.filter(Role.name==del_role).first())
            db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    product_power = db.Column(db.Integer(), nullable=False)
    product_item = db.Column(db.Integer(), unique=True)
    product_weight = db.Column(db.Integer(), nullable=False)
    product_material = db.Column(db.String(255, collation='NOCASE'))

    def __init__(self, product_name, product_power, product_item, product_weight, product_material):
        self.product_name = product_name
        self.product_power = product_power
        self.product_item = product_item
        self.product_weight = product_weight
        self.product_material = product_material

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer(), primary_key=True)
    component_name = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    component_unit = db.Column(db.String(255, collation='NOCASE'))
    component_item = db.Column(db.Integer(), unique=True)

    def __init__(self, component_name, component_unit, component_item):
        self.component_name = component_name
        self.component_unit = component_unit
        self.component_item = component_item

class Specification(db.Model):
    __tablename__ = 'specification'
    id = db.Column(db.Integer(), primary_key=True)
    component_type = db.Column(db.String(255, collation='NOCASE'))
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id', ondelete='CASCADE'))
    component_id = db.Column(db.Integer(), db.ForeignKey('component.id', ondelete='CASCADE'))
    count =  db.Column(db.Float())

    def __init__(self, component_type, product_id, component_id, count):
        self.component_type = component_type
        self.product_id = product_id
        self.component_id = component_id
        self.count = count
    
    def get_component(self):
        return Component.query.filter(Component.id == self.component_id).first()
    
    def get_product(self):
        return Product.query.filter(Product.id == self.product_id).first()
    


