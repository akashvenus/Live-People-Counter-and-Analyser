from tkinter import *
from tkcalendar import *
import _thread
import os
import sys
import mysql.connector
import pandas as pd
from front import work
from aisle import work2

root = Tk()
root.resizable(width=False, height=False)
root.title("Sample tkinter")
root.geometry(r"550x550")
root.config(bg="#4CAD3B")


def open_entry():
    os.system("db1.py")

def open_aisle():
    os.system("db2.py")

def close_entry():
    os.system("db10.py")

def close_aisle():
    os.system("db20.py")

def run_entry():
    _thread.start_new_thread(work,())
    _thread.start_new_thread(work2,())

def openNewWindow(button):
    global createdb_btn
    newWindow = Toplevel(root)
    newWindow.protocol("WM_DELETE_WINDOW", lambda:(button.config(state='active'), newWindow.destroy()))
    newWindow.resizable(width=False,height=False)
    newWindow.title("New Window")
    newWindow.geometry("300x300")

    create_front = Button(newWindow,text="Entry DB",relief=FLAT,bg="black",fg="white",command=open_entry)
    create_front.place(x=50,y=80)

    create_aisle = Button(newWindow,text="Aisle DB",relief=FLAT,bg="black",fg="white",command=open_aisle)
    create_aisle.place(x=145,y=80)

def openAnotherWindow(button):
    global removedb_btn
    otherWindow = Toplevel(root)
    otherWindow.protocol("WM_DELETE_WINDOW", lambda:(button.config(state='active'), otherWindow.destroy()))
    otherWindow.resizable(width=False,height=False)
    otherWindow.title("Another Window")
    otherWindow.geometry("300x300")
    remove_front = Button(otherWindow,text="Entry DB",relief=FLAT,bg="black",fg="white",command=close_entry)
    remove_front.place(x=50,y=80)

    remove_aisle = Button(otherWindow,text="Aisle DB",relief=FLAT,bg="black",fg="white",command=close_aisle)
    remove_aisle.place(x=145,y=80)

def firstAnalyser():
    an1 = Toplevel(root)
    an1.title("First Analyser")
    an1.resizable(width=False,height=False)
    an1.geometry("500x550")
    an1.config(bg="#cd950c")
    hour_string=StringVar()
    min_string=StringVar()
    last_value_sec = ""
    last_value = ""
    f = ('Times', 15)
    date1 = ""
    date2 = ""
    time1 = ""
    time2 = ""

    def firstTime():
        global date1
        global time1
        date1 = cal.get_date()
        h = min_sb.get()
        m = sec_hour.get()
        s = sec.get()
        time1 = str(f"{h}:{m}:{s}")
        t1 = f"starting date and time is {date1} at {h}:{m}:{s}."
        msg_display.config(text=t1)

    def secondTime():
        global date2
        global time2
        date2 = cal.get_date()
        h = min_sb.get()
        m = sec_hour.get()
        s = sec.get()
        time2 = str(f"{h}:{m}:{s}")
        t2 = f"ending date and time is {date2} at {h}:{m}:{s}."
        msg_display.config(text=t2)


    def runAnalyser1():
        global date1
        global date2
        global time1
        global time2
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "mydatabase"
        )
        df = pd.read_sql("SELECT * FROM details",db)
        df['datetime'] = pd.to_datetime(df['Day'] + ' ' + df['InTime'])
        filter = df.loc[df['datetime'].between(f'{date1} {time1}', f'{date2} {time2}'), 'count']
        print (len(filter))

    if last_value == "59" and min_string.get() == "0":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)
        last_value = min_string.get()

    if last_value_sec == "59" and sec_hour.get() == "0":
        min_string.set(int(min_string.get())+1 if min_string.get() !="59" else 0)

    if last_value == "59":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)
        last_value_sec = sec_hour.get()


    fone = Frame(an1)
    ftwo = Frame(an1)

    fone.pack(pady=10)
    ftwo.pack(pady=10)

    cal = Calendar(fone, selectmode="day", year=2021, month=1,day=1)
    cal.pack()

    min_sb = Spinbox(ftwo,from_=0,to=23,wrap=True,textvariable=hour_string,width=2,state="readonly",font=f,justify=CENTER)
    sec_hour = Spinbox(ftwo,from_=0,to=59,wrap=True,textvariable=min_string,font=f,width=2,justify=CENTER)

    sec = Spinbox(ftwo,from_=0,to=59,wrap=True,textvariable=sec_hour,width=2,font=f,justify=CENTER)

    min_sb.pack(side=LEFT, fill=X, expand=True)
    sec_hour.pack(side=LEFT, fill=X, expand=True)
    sec.pack(side=LEFT, fill=X, expand=True)

    msg = Label(an1, text="Hour  Minute  Seconds",font=("Times", 12),bg="#cd950c")
    msg.pack(side=TOP)

    startingBtn =Button(an1,text="Starting date",padx=10,pady=10,command=firstTime)
    startingBtn.pack(pady=10)

    endingBtn =Button(an1,text="Ending date",padx=10,pady=10,command=secondTime)
    endingBtn.pack(pady=10)

    sendBtn = Button(an1,text="Send",padx=10,pady=10,command=runAnalyser1)
    sendBtn.pack(pady=10)

    msg_display = Label(an1,text="",bg="#cd950c")
    msg_display.pack(pady=10)

def secondAnalyser():
    an2 = Toplevel(root)
    an2.title("Second analyser")
    an2.resizable(width=False,height=False)
    an2.geometry("500x550")
    an2.config(bg="#cd950c")
    date11 = ""
    date22 = ""

    def firstDate():
        global date11
        date11 = cal.get_date()
        t1 = f"starting date is {date11}"
        msg_display.config(text=t1)

    def secondDate():
        global date22
        date22 = cal.get_date()
        t2 = f"ending date is {date22}"
        msg_display.config(text=t2)

    def forBetween():
        global date11
        global date22
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "mydatabase"
        )
        df = pd.read_sql("SELECT * FROM aisles",db)
        df["Day"] = pd.to_datetime(df["Day"])
        df.set_index('Day', inplace=True)
        print((df.loc[date11:date22]).sum())

    fram1 = Frame(an2)

    fram1.pack(pady=10)

    cal = Calendar(fram1, selectmode="day", year=2021, month=1,day=1)
    cal.pack()


    onedayBtn =Button(an2,text="Starting date",padx=10,pady=10,command=firstDate)
    onedayBtn.pack(pady=10)

    seconddayBtn =Button(an2,text="Ending date",padx=10,pady=10,command=secondDate)
    seconddayBtn.pack(pady=10)

    cnfBtn = Button(an2,text="Confirm",padx=10,pady=10,command=forBetween)
    cnfBtn.pack(pady=10)

    msg_display = Label(an2,text="",bg="#cd950c")
    msg_display.pack(pady=10)

def help_open():
    os.system("help.txt")


heading = Label(root,text="Navigation Screen",font=("Arial",20),bg="#4CAD3B")
heading.place(x=165,y=10)

camera_btn = Button(root,text="Open Cams",relief=FLAT,bg="black",fg="white",font=("Times",12),command=run_entry)
camera_btn.place(x=50,y=180)

createdb_btn = Button(root,text="Create databases",relief=FLAT,bg="black",fg="white",font=("Times",12))
createdb_btn.config(command=lambda b=createdb_btn: (openNewWindow(b), b.config(state='disabled')))
createdb_btn.place(x=205,y=180)

removedb_btn = Button(root,text="Remove databases",relief=FLAT,bg="black",fg="white",font=("Times",12))
removedb_btn.config(command=lambda b=removedb_btn: (openAnotherWindow(b), b.config(state='disabled')))
removedb_btn.place(x=380,y=180)

entry_analy = Button(root,text="Analyser 1",relief=FLAT,bg="black",fg="white",font=("Times",12),command=firstAnalyser)
entry_analy.place(x=55,y=340)

inside_analy = Button(root,text="Analyser 2",relief=FLAT,bg="black",fg="white",font=("Times",12),command = secondAnalyser)
inside_analy.place(x=210,y=340)

hlp_btn = Button(root,text="Help",relief=FLAT,bg="black",fg="white",font=("Times",12),command = help_open)
hlp_btn.place(x=390,y=340)

root.mainloop()
