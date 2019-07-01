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
    components =  db.relationship('Component', secondary='product_components')

class ProductComponents(db.Model):
    __tablename__ = 'product_components'
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id', ondelete='CASCADE'))
    component_id = db.Column(db.Integer(), db.ForeignKey('component.id', ondelete='CASCADE'))

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer(), primary_key=True)
    detail = db.relationship('Detail', secondary='details')
    component_count = db.Column(db.Integer())

class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer(), primary_key=True)
    detail_name = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    cost = db.Column(db.Integer())

class StockComponents(db.Model):
    __tablename__ = 'stock_components'
    id = db.Column(db.Integer(), primary_key=True)
    stock_id = db.Column(db.Integer(), db.ForeignKey('stock.id', ondelete='CASCADE'))
    component_id = db.Column(db.Integer(), db.ForeignKey('component.id', ondelete='CASCADE'))


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer(), primary_key=True)
    components = db.relationship('Component', secondary='stock_components')