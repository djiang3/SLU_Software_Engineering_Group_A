import sqlite3 as lite

""" Here is the initial routine to open and insert data into our database. See documentation at http://zetcode.com/db/sqlitepythontutorial/"""

con = lite.connect('Database_GroupA.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("DROP TABLE IF EXISTS Stocks")
    cur.execute("CREATE TABLE Tweets(user TEXT, message TEXT, date TEXT)")
    cur.execute("INSERT INTO Tweets VALUES('User1', 'Message1', 'Date1')")
    cur.execute("INSERT INTO Tweets VALUES('User2', 'Message2', 'Date2')")
    cur.execute("CREATE TABLE Stocks(id INTEGER PRIMARY KEY, timestamp INTEGER, symbol TEXT, price REAL)")
    cur.execute("SELECT * FROM Tweets")
    rows = cur.fetchall()
    
    for row in rows:
        print row