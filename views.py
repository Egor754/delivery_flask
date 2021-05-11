from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db, manager
from forms import OrderForm, RegisterForm, LoginForm
from models import Food, Category, User, Orders


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main_view():
    category = db.session.query(Category).all()
    return render_template('delivery/main.html', category=category)


@app.route('/addtocart/<int:pk>/')
def add_to_cart(pk):
    food = Food.query.get_or_404(pk)
    cart = session.get("cart", [])
    if pk not in cart:
        cart.append(pk)
        session['cart'] = cart
    flash('Товар добавлен в корзину')
    return redirect(url_for('cart_view'))


@app.route('/deltocart/<int:pk>/')
def del_to_cart(pk):
    try:
        session['cart'].remove(pk)
        flash('Товар удален из корзины')
    except ValueError:
        flash('Такого товара нет в корзине')
    return redirect(url_for('cart_view'))


@app.route('/cart/', methods=['GET', 'POST'])
def cart_view():
    form = OrderForm()
    foods = Food.query.filter(Food.id.in_(session['cart']))
    if request.method == 'POST' and form.validate_on_submit() and current_user.is_authenticated:
        if not foods:
            flash('Вы ничего не выбрали')
            return render_template('delivery/cart.html', form=form)
        orders = Orders(
            amount=sum(sub.price for sub in foods),
            status='good',
            phone=form.phone.data,
            address=form.address.data,
            user=User.query.get(current_user.get_id())
        )
        db.session.add(orders)
        for food in foods:
            orders.food.append(food)
        db.session.commit()
        session.pop('cart',None)
        return redirect(url_for('ordered_view'))
    return render_template('delivery/cart.html', form=form)


@app.route('/account/')
@login_required
def account_view():
    orders = Orders.query.filter(Orders.user_id == current_user.get_id())
    return render_template('delivery/account.html', orders=orders)


@app.route('/register/', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter(User.mail == form.email.data).first():
            form.email.errors.append("Такой пользователь уже существует")
            return render_template('delivery/register.html', form=form)
        user = User(mail=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_view'))
    return render_template('delivery/register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user and user.password_valid(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main_view'))
        else:
            form.email.errors.append("Не верное имя или пароль")
    return render_template('delivery/login.html', form=form)


@app.route('/logout/')
def logout_view():
    logout_user()
    return redirect(url_for('main_view'))


@app.after_request
def redirect_to_signin(respons):
    if respons.status_code == 401:
        return redirect(url_for('login_view') + '?next=' + request.url)
    return respons


@app.route('/ordered/')
def ordered_view():
    return render_template('delivery/ordered.html')


@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Страничка не найдена</h1>", 404


@app.errorhandler(500)
def server_error(error):
    return "<h1>Всё очень плохо</h1>", 500
