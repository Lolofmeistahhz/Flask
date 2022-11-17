import datetime

from appivt import app
from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g

from appivt.bd_exe import connect_db, FDataBase

menu = [{'title': 'Главная', 'url': 'index'}, {'title': 'Блюда', 'url': 'dishes'}, {'title': 'Помощь', 'url': 'help'},
        {'title': 'Контакт', 'url': 'contact'}, {'title': 'Авторизация', 'url': 'login'},{'title':'Регистрация','url':'reg'}]


app.permanent_session_lifetime = datetime.timedelta(seconds=20)

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()


@app.route('/index_db')
def index_db():
    db = get_db()
    db = FDataBase(db)
    return render_template('index_db.html',title = 'Index_db', menu=db.getMenu(),post=db.getPosts())



@app.route('/index')
def index():
    best_ivt = {'username': 'Шляпкин'}
    favorite_writes = [{'author': {'username': 'Tolkien'},
                        'body': ' Lords of the ring'
                        },
                       {'author': {'username': 'Pushkin'},
                        'body': ' Capitans of the daughter'
                        },
                       {'author': {'username': 'Lermontov'},
                        'body': ' Парус'
                        }]

    return render_template('index.html', title='2022 Forever', user=best_ivt, favorite_writes=favorite_writes,
                           menu=menu)


@app.route('/dishes')
def dish():
    best_user = {'username': 'Николай'}
    favorite_dishes = [{'name': {'dishname': 'Fried chicken'},
                        'ingridients': {'ingr1': 'Meat of chicken',
                                        'ingr2': 'some spicy sauce'},
                        'photo': 'https://hi-news.ru/wp-content/uploads/2020/06/chicken_home_image_one-750x558.jpg'}]

    return render_template('dishes.html', title='2022 Forever', abuser=best_user, favorite_dishes=favorite_dishes,
                           menu=menu)


@app.route('/help')
def help():
    return render_template('help.html', title='Cправка', menu=menu)


def rec(bd, f):
    print(f['username'])
    bd.append({'username': f['username'], 'message': f['message']})

def rec_reg(bd,f):
    print(f['username'], f['psw'])
    bd.append({'username': f['username'], 'psw': f['psw']})


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
            rec(bd_contact, request.form)
        else:
            flash('Ошибка отправки', category='error')
        print(get_flashed_messages(True))
        print(request.form['username'])
        print(bd_contact)

    return render_template('contact.html', title='Контакты', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST':
        for item in db.getUser():
            if item['username'] == request.form['username'] and item['password'] == request.form['psw']:
                session['userlogged'] = request.form['username']
                return redirect(url_for('profile', username=session['userlogged']))
        else:
            pass
    return render_template('login.html', title='Авторизация', menu=menu, data=db.getUser())

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        db.add_users(request.form['username'],request.form['psw'])
    return  render_template('reg.html', title='Регистрация', menu=menu)

@app.route('/profile/<username>')
def profile(username):
   if 'userlogged' not in session or session['userlogged'] != username:
       abort(401)
   return f'<h3>Пользователь : {username}</h3>'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Все сломалось', menu=menu)

@app.errorhandler(401)
def page_error_401(error):
    return render_template('page401.html', title='Ошибка авторизации', menu=menu)


