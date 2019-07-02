from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,  SelectField, FloatField

from wtforms import validators, ValidationError

class ProductForm(Form):
    name = TextField("Наименование изделия",[validators.Required("Введите наименование изделия")])
    item = IntegerField("Артикул")
    power = IntegerField("Мощность", [validators.Required("Введите мощность изделия")])
    materials = SelectField('Материалы', choices = [('Стекло','Стекло'),  ('Пластик','Пластик')])
    unit = IntegerField("Единица измерения")
    weight = FloatField('Вес', [validators.Required("Введите вес изделия")])
    submit = SubmitField("Добавить")

class ComponentForm(Form):
    name = TextField("Наименование комплектующего",[validators.Required("Введите наименование изделия")])
    unit = TextField("Единица измерения",[validators.Required("Введите единицу измерения")])
    item = IntegerField("Артикул")
    submit = SubmitField("Добавить")

