# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
connect = sqlite3.connect("frequencies.db")
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS frequencies")
cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,\
                    CSharp float,\
                    D  float,\
                    DSharp float,\
                    E float,\
                    F float,\
                    FSharp float,\
                    G float,\
                    GSharp float,\
                    A      float,\
                    ASharp float,\
                    B float\
);")


f0=27.50
for i in range(-1,9):
    frequencies=[]
    octave=[]
    octave.append(i)
    for j in range (-9,3) :
        frequency=f0*2**(j/12)
        octave.append(frequency)
    frequencies.append(octave)
    f0=f0*2
    cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)

connect.commit()
