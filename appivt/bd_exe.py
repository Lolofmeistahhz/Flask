import sqlite3
from appivt import app



menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Блюда', 'url': 'dishes'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Контакт', 'url': 'contact'}, {'name': 'Авторизация', 'url': 'login'},{'name':'Регистрация','url':'reg'}]

bd_userdata=[{'username':'test','psw':'test'},{'username':'root','psw':'pass'},{'username':'log','psw':'psw'}]

posts=[{'title':'test','post_message':'test'},{'title':'test2','post_message':'test2'},{'title':'test3','post_message':'test3'}]

def connect_db():
    '''создание соединения с бд'''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогательная функция для создания таблицы'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db1):
        self.__db = db1
        self.__cursor = db1.cursor()

    def add_menu(self, title, url):
        try:
            self.__cursor.execute("insert into mainmenu values(NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True

    def add_users(self, username, psw):
        try:
            self.__cursor.execute("insert into users values(NULL, ?, ?)", (username, psw))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True

    def add_post(self, title, post_message):
        try:
            self.__cursor.execute("insert into post values(NULL, ?, ?)", (title, post_message))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД " + str(e))
            return False
        return True

    def del_menu(self,id=0):
        if id == 0:
            self.__cursor.execute("delete from mainmenu ")
            self.__db.commit()
        else:
            self.__cursor.execute(f"delete from mainmenu where id={id}")

    def getMenu(self):
        sql = 'SELECT * FROM mainmenu'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')
        return()

    def getUser(self):
        sql = 'SELECT * FROM users'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')

    def getPosts(self):
        sql = 'SELECT * FROM post'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')
        return ()



if __name__ == "__main__":
    db = connect_db()
    db = FDataBase(db)
    for i in bd_userdata:
        print(db.add_users(i['username'], i['psw']))
    for i in menu:
        print(db.add_menu(i['name'], i['url']))
    for i in posts:
        print(db.add_post(i['title'], i['post_message']))