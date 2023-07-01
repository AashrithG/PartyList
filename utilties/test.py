from tkinter import *
import sqlite3

root = Tk()

def myClick():
    info = myEntry.get()
    con = sqlite3.connect("tes.db")
    cursor = con.cursor()
    try:
        cursor.execute("CREATE TABLE info(thing)")
    except:
        pass
    cursor.execute(f"""
    INSERT INTO info VALUES
        ('{info}')
    """)
    con.commit()
    con.close()

myEntry = Entry(root)
myEntry.pack()

myButton = Button(root, text="Click Me!", command=myClick)
myButton.pack()

root.mainloop()
