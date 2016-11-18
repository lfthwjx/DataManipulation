import sqlite3

conn = sqlite3.connect('whatever.db',timeout=10)
c1 = conn.cursor()
c1.execute("CREATE TABLE SI(ID INT PRIMARY KEY NOT NULL,NAME TEXT NOT NULL, AGE INT NOT NULL)")
c1.execute("INSERT INTO SI VALUES (93,'James King',18)")
conn.commit()
conn.close()
c1.execute("SELECT * FROM si")

c1.fetchall()
for row in c1:
    print row
#c1.commit()


conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),('2006-04-06', 'SELL', 'IBM', 500, 53.00),]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
conn.commit()
results = c.execute('SELECT * FROM stocks ORDER BY price')
for row in results:
    print row

results.fetchall()
