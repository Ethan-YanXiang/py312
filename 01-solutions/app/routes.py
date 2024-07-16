# 從 py檔(模組) 調用 實例
from app import app  # from __init__.py import Flask(__name__)

from flask import render_template, request, current_app, make_response, abort
from datetime import datetime
import random
# 從 包 調用 模組


# (Parametrized or Dynamic) Routes
@app.route('/<name>')  # '/<int:num>'
def name_func(name):  # view function, business logic

    if len(name) > 20:
        abort(400)  # throws an exception

    return render_template('name.html', name=name)
    # normally returns an HTML page as response


@app.route('/')  # calling method to connect '/' address to view function
@app.route('/index')
def home_func():
    now = datetime.now()

    response = make_response('Cookie onboard!')
    response.set_cookie('answer', '42')

    return render_template('index.html', title='datetime', now=now, response=response)


@app.route('/random')
def quotes_func():
    with app.open_resource('data/quotes.txt', 'r') as file:
        quotes = file.read().split('\n')
    random_quote = random.choice(quotes)
    return render_template('quotes.html', title='random_quote', random_quote=random_quote)


def is_prime(num):  # 是否是質數
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def collect_prime_divisors(num):  # 蒐集是質數也是除數的數
    divisors = []
    for i in range(2, num + 1):
        if num % i == 0 and is_prime(i):
            divisors.append(i)
    return divisors


@app.route('/prime_divisors', methods=['GET', 'POST'])
def prime_func():
    try:
        if request.method == 'POST':
            num = int(request.form['num'])  # saving the key in num
            factors = collect_prime_divisors(num)
            return render_template('prime.html', title='get_prime_divisors', num=num, factors=factors)
    except ValueError:
        pass

    return render_template('prime.html')  # when fetching the page first time (GET)


@app.route('/app_object', methods=['GET'])
def app_func():
    app_object = current_app.config
    return render_template('app.html', title='app_object', app_object=app_object, current_app=current_app)


@app.route('/request_object', methods=['GET'])
def request_func():
    user_agent = request.headers.get
    return render_template('request.html', title='request_object', user_agent=user_agent, request=request)
