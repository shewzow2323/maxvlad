
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, make_response, redirect, session
import psycopg2
import os
lab5 = Blueprint("lab5",__name__)





def dbConnect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='knowledge_base_for_vlad',
        user='postgres',
        password='postgres'
    )
    return conn

def dbClose(cur, con):
    cur.close()
    con.close()

@lab5.route("/lab5/")
def main():
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute('select * from users;')
    result = cur.fetchall()

    print(result)

    dbClose(cur, conn)

    return render_template('lab5.html')





@lab5.route('/lab5/register', methods=["GET","POST"])
def registerPage():
    errors = []
    if request.method == "GET":
        return render_template("register.html", errors=errors)
    

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        print (errors)
        return render_template("register.html", errors=errors)
    hashPassword=generate_password_hash(password)
    
    conn = dbConnect()
    cur = conn.cursor()
    
    cur.execute(f"select username from users where username = '{username}';")

    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")
        cur.close()
        conn.close()
        return render_template("register.html", errors=errors)
    
    cur.execute(f"insert into users (username, password) values ('{username}','{hashPassword}');")

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/lab5/login5')




@lab5.route("/lab5/login5", methods=['GET','POST'])
def loginPage():
    errors = [];
    if request.method == "GET":
        return render_template("login5.html", errors=errors)
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        return render_template("login5.html", errors=errors)


    conn = dbConnect()
    cur = conn.cursor()

    cur.execute(f"select id, password from users where username = '{username}'")

    result=cur.fetchone()

    if result is None:
        errors.append("Неправильный логин или пароль")
        dbClose(cur,conn)
        return render_template("login5.html", errors=errors)
    
    userID, hashPassword = result

   
    if check_password_hash(hashPassword, password):
        session['id'] = userID
        session['username'] = username
        dbClose(cur, conn)
        return redirect("/lab5/new_article")
    else:
        errors.append("Неправильный пароль или логин")
        return render_template("login5.html", errors=errors)

    


    

@lab5.route("/lab5/new_article")
def createArticle():
    errors=[]
    userID = session.get("id")

    if userID is not None:
        if request.method =='GET':
            return render_template("new_article.html")
    
        if request.method =='POST':
            title = request.form.get("title_article")
            text_article= request.form.get("text_article")
        
        if len(text_article) == 0:
            errors=['Заполните текст']
            return render_template('new_article.html', errors=errors)
        
        conn, cur = dbConnect()

        cur.execute(f"INSERT INTO articles (user_id, title, article_text) VALUES ({userID}, '{title}', '{text_article}') RETURNING id")
        new_article_id = cur.fetchone()[0]
        conn.commit()

        dbClose(conn, cur)
        return redirect(f"/lab5/new_article/{new_article_id}")
    return redirect("/lab5/login5")

def dbConnect():
    try:
        conn = psycopg2.connect(
            database="knowledge_base_for_vlad",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            
        )
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None, None
        
@lab5.route("/lab5/new_article",methods=['POST'])
def getArticle(article_id):
    userID = session.get('id')

    if userID is not None:
        conn=dbConnect()
        conn, cur = dbConnect()


    cur.execute(f"SELECT title, article_text FROM articles WHERE id = {article_id} and user_id = {userID}")
    articleBody = cur.fetchone()

    dbClose(cur, conn)
    if articleBody is None:
        return 'Not found!'
    
    text= articleBody[1].splitlines()
    

    return render_template("new_article.html", article_text=text, article_title=articleBody[0], username=session.get('username'))

@lab5.route("/lab5/articles")
def getArticles():
    userID = session.get("id")
    
    if userID is not None:
        conn, cur = dbConnect()
        
        cur.execute(f"SELECT title, article_text FROM articles WHERE user_id = {userID}")
        articles = cur.fetchall()
        
        dbClose(conn, cur)
        
        return render_template("articles.html", articles=articles)
    else:
        return redirect("/lab5/login5")

if __name__ == "__main__":
    lab5.run(debug=True)