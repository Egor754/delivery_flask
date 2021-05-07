import phonenumbers as phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Email


class OrderForm(FlaskForm):
    name = StringField('Имя', [InputRequired(message="Введите что-нибудь")])
    address = StringField('Адрес', [InputRequired(message='Введите адрес')])
    phone = StringField('Телефон', [InputRequired()])
    submit = SubmitField('Оформить заказ')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Некорректный номер')


class RegisterForm(FlaskForm):
    email = StringField("Электропочта", [
        Email(message="Это не похоже на почту, попробуйте еще раз!"),
        DataRequired(message='Это поле обязательное'),
    ])
    password = PasswordField('Пароль', [
        DataRequired(message='Это поле обязательное'),
        Length(min=5, message="Пароль должен быть не менее 5 символов"),
    ])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField("Электропочта", [DataRequired(message='Это поле обязательное')])
    password = PasswordField('Пароль', [DataRequired(message='Это поле обязательное')])
    submit = SubmitField('Зарегистрироваться')
