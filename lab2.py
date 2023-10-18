from flask import Blueprint, redirect, url_for, render_template

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/example/')
def example():
    name = 'Кривошеев М.С., Гавра В.А.' 
    lab_num = 'Лабораторная работа 2'
    group = 'ФБИ-11'
    course = '3 курс'
    fruits = [
      {'name':'яблоки', 'price':100},
      {'name':'груши', 'price':120},
      {'name':'апельсины', 'price':80},
      {'name':'мандарины', 'price':95},
      {'name':'манго', 'price':375},
    ]
    books = [
      {'name':'Остров сокровищ', 'price':328},
      {'name':'Повесть временных лет', 'price':1000},
      {'name':'Неизведанное', 'price':3392},
      {'name':'Корабль', 'price':32494},
      {'name':'Анонс', 'price':4833},
    ]
    return render_template('example.html')

@lab2.route('/lab2/')
def lab__2():
    return render_template('lab2.html')


@lab2.route('/lab2/smex/')
def smex():
    return render_template('smex.html')


