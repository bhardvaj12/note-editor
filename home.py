from tkinter import *
import mysql.connector
connection = mysql.connector.connect(host="localhost",user="root",password="",database="notepad")
dbcursor = connection.cursor()

def home(root,header,body):
    root.minsize(400,550)
    root.maxsize(400,550)
    for w in header.winfo_children():
        w.destroy()
    for w in body.winfo_children():
        w.destroy()
    login_tab = Button(header,text="Login",font=("Arial",12,"bold"),width=20,height=2,bg="#666",bd=0,fg="#fff",command=login_tab_view)
    login_tab.pack(side=LEFT,pady=0,padx=0,ipady=0)
    register_tab = Button(header,text="Register",font=("Arial",12,"bold"),width=20,height=2,bg="#666",bd=0,fg="#fff",command=registration_tab_view)
    register_tab.pack(side=RIGHT,padx=1,pady=0)

    login_tab_view()

def notepad():
    global header
    global body
    global root
    for part in header.winfo_children():
        part.destroy()
    for part in body.winfo_children():
        part.destroy()
    root.maxsize(1920,1080)
    root.minsize(1920,1080)
    # root.attributes("-fullscreen",True)
    root.title("NotePad")


    
def notehome(email,password):
    global dbcursor
    print("Arrived!!!")
    print(email," ",password)
    dbcursor.execute("SELECT * from users WHERE email = '{}' AND passwd = '{}' ;".format(email,password))
    if dbcursor.fetchone() :
        notepad()

def login_tab_view():
    global root
    global body
    global header
    root.title("Login")
    for w in body.winfo_children():
        w.destroy()
    print("login")

    email_entry = Entry(body,width = 100,text="enter email",font=("Arial",12,"bold"))
    email_entry.pack(side =TOP,pady=(100,10),padx=50,ipadx=5,ipady=5)
    password_entry = Entry(body,width = 100,text="enter password",font=("Arial",12,"bold"))
    password_entry.pack(side=TOP,pady=10,padx=50,ipadx=5,ipady=5)
    log_me_in = Button(body,text="Login",font=("Arial",12,"bold"),width=30,height=2,bg="#224",bd=0,fg="#fff",command =lambda: notehome(email_entry.get(),password_entry.get()))
    log_me_in.pack(side=TOP,padx=80,pady=(10,250))

def register(username,email,password):
    print(username)
    print(email)
    print(password)

def registration_tab_view():
    global root
    root.title("Registration")
    for w in body.winfo_children():
        w.destroy()
    print("registration")
    username_entry = Entry(body,width = 100,text="username",font=("Arial",12,"bold"))
    username_entry.pack(side =TOP,pady=(100,10),padx=50,ipadx=5,ipady=5)
    email_entry = Entry(body,width = 100,text="enter email",font=("Arial",12,"bold"))
    email_entry.pack(side =TOP,pady=10,padx=50,ipadx=5,ipady=5)
    password_entry = Entry(body,width = 100,text="enter password",font=("Arial",12,"bold"))
    password_entry.pack(side=TOP,pady=10,padx=50,ipadx=5,ipady=5)
    register_me_in = Button(body,text="Register",font=("Arial",12,"bold"),width=30,height=2,bg="#224",bd=0,fg="#fff",command =lambda: register(username_entry.get(),email_entry.get(),password_entry.get()))
    register_me_in.pack(side=TOP,padx=80,pady=(10,200))

root = Tk()
header = Frame(root)
header["height"] = 50
header["width"] = 400
header["bg"]="#224"
header.pack(side=TOP)
body = Frame(root)
body["height"] = 800
body["width"] = 400
body["bg"]= "#222"
body.pack(side=TOP)

# login/registration

home(root,header,body)

root.mainloop()
