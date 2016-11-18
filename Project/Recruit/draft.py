#!/usr/bin/python
import peewee
from peewee import *
import MySQLdb
import mysql.connector
cnx = mysql.connector.connect(user='root', password='wanjun',host='127.0.0.1')
cur = cnx.cursor()
cur.execute("CREATE DATABASE test")
cur.execute('''CREATE TABLE test.test(
               name VARCHAR(50),
               age INTEGER)''')
cur.execute('''INSERT INTO test.test VALUE("James",18) ''')
cnx.commit()
sql = '''CREATE TABLE foo (
       bar VARCHAR(50) DEFAULT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cur.execute(sql)
cur.execute("SELECT * FROM test.test")
cur.fetchall()
cur.close()

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="wanjun",  # your password
                     db="test")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM test")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()
db = MySQLDatabase('localhost', user='root',passwd='wanjun',db='test')

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()
for book in Book.filter(author="me"):
    print book.title


json_data = json.loads(data)
json_data['content']['positionResult'].keys()