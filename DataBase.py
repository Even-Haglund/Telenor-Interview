import sqlite3
import traceback
 
#create/connect to the SQLite Database
con = sqlite3.connect("database.db", check_same_thread=False, timeout=200)
cur = con.cursor()


#get the count of tables with the name "Ansatte"
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Telenor' ''')
#if the count is 1, then table exists, if not create it
if cur.fetchone()[0]!=1 :{
    cur.execute("""CREATE Table Telenor (
            ADRESSEID FLOAT(8),
            fylke VARCHAR,
            kommune VARCHAR,
            BYGNINGSTYPE VARCHAR,
            Lat FLOAT(15, 13),
            Lon FLOAT(15, 13),
            PRIMARY KEY (ADRESSEID))""")
}
    
FileToGoThrough = open("AdresserUtsira.csv", "r")
for lines in FileToGoThrough:
    print(lines)
    try: 
        Info = lines.split(";")
        cur.execute("INSERT INTO Telenor VALUES (?, ?, ?, ?, ?, ?)", Info)
        con.commit()
    except:
        traceback.print_exc()
        continue