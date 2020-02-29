from tkinter import *
import os
import shutil
import time
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
connection = mysql.connector.connect(host="localhost",user="root",password="",database="notepad")
dbcursor = connection.cursor()

class User:
    """
        this class records the details of user which is currently active.
    """
    def __init__(self,user_data=None):
        if user_data is None:
            self.UID = 1
            self.name = "user1"
            self.email = "user1@mail.com"
            self.password = "user1password"
        else:
            self.UID = user_data[0]
            self.name = user_data[1]
            self.email = user_data[2]
            self.user = user_data
    
    def __str__(self):
        return f"({self.UID})"

def home():
    """
        this function is the home page of the app
        > resize the window and setup
        > clear the root window
        > add buttons for login and registration
        > call the login_view_tab to show login window
    """
    root.minsize(400,550)
    root.maxsize(400,550)
    header["height"] = 50
    header["width"] = 400
    header["bg"]="#224"
    
    body["height"] = 800
    body["width"] = 400
    body["bg"]= "#222"
    
    for w in header.winfo_children():
        w.destroy()
    for w in body.winfo_children():
        w.destroy()
    
    login_tab = Button(header,text="Login",font=("Arial",12,"bold"),width=20,height=2,bg="#666",bd=0,fg="#fff",command=lambda: login_tab_view(login_tab,register_tab))
    login_tab.pack(side=LEFT,pady=0,padx=0,ipady=0)

    register_tab = Button(header,text="Register",font=("Arial",12,"bold"),width=20,height=2,bg="#666",bd=0,fg="#fff",command=lambda: registration_tab_view(login_tab,register_tab))
    register_tab.pack(side=RIGHT,padx=1,pady=0)
    
    login_tab_view(login_tab,register_tab)

def notepad(current_user):
    """
         this window is after login:
         > destroy the header frame which previously contained login and registration button
         > destroy body
         > resize window and few tweaks to the window
         > fetch all the text files from the database associated with the user
         > check if there is any files created and act accordingly
         > if there are files associated with the user create a listbox to show it
         > add create , open , delete and logout button
    """
    for part in header.winfo_children():
        part.destroy()
    
    for part in body.winfo_children():
        part.destroy()
    print(current_user)
    root.maxsize(1600,900)
    root.minsize(1600,900)
    body["height"] = 50
    body["width"] = 1600
    header["height"] = 850
    header["width"] = 1600
    root.title("NotePad")

    dbcursor.execute(f"SELECT * from notes WHERE UID = '{current_user.UID}'")
    documents = dbcursor.fetchall()
    if documents == []:
        label_warning =Label(header,text = "No file in Existence for you!!! \n you can create a new file by clicking on 'New'",font=("Arial",12,"bold"),fg="#900",bg="#224")
        label_warning.pack(side=TOP,padx=624,pady=400)
    else:
        doclist = Listbox(header,width=174,height = 41,selectmode=SINGLE,font=("Arial",12,"bold"),fg="#ccc",bg="#222")
        # print(documents)
        doclist.pack(side=LEFT,padx=5,pady=5)
        for docs in documents:
            doclist.insert(END,docs[1])
            doclist.itemconfig
        scrollbar = Scrollbar(header)
        scrollbar.pack(side=RIGHT,fill=Y)
        doclist.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command=doclist.yview)
    
    create_new_file = Button(body,text = "NEW",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: create_new_file_window(current_user))
    create_new_file.pack(side=LEFT,pady=7,ipady=5,ipadx=5,padx=150)
    try:
        open_file = Button(body,text = "OPEN",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: note_editor(doclist.get(ANCHOR),current_user))
        open_file.pack(side=LEFT,pady=7,ipady=5,ipadx=5,padx=150)
        delete_file = Button(body,text = "DELETE",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: delete_data(doclist.get(ANCHOR),current_user))
        delete_file.pack(side=LEFT,pady=7,ipady=5,ipadx=5,padx=150)
    except:
        messagebox.showinfo("Alert","you have no file to open!!!")
    logout_button = Button(body,text = "LOGOUT",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = home)
    logout_button.pack(side=LEFT,pady=10,ipady=7,ipadx=5,padx=110)

def delete_data(filename,current_user):
    """
        this function takes in two arguments current user and filename to be deleted.
        > check if there is something selected or just a prank
        > if there is then delete the filename from notes table in the database
        > then use shutil to move the file from 'notes' folder to 'deleted' folder == because we dont lose data.
    """

    if filename is not None and current_user is not None:
        try:
            dbcursor.execute(f"DELETE FROM notes WHERE filename = '{filename}' AND UID = '{current_user.UID}'")
            connection.commit()
        except:
            print("some error occured!!!")
        else:
            try:
                filename = filename + ".txt"
                shutil.move(os.path.join(os.getcwd(),"notes",filename),os.path.join(os.getcwd(),"deleted"))
            except FileNotFoundError:
                pass
            # os.rename(os.path.join(os.getcwd(),"notes",filename),os.path.join(os.getcwd(),"notes"))
    notepad(current_user)

def create_new_file_window(current_user):

    """
        this window creates a new file in the user system
        > ask for the filename through a dialog box
        > handle errors accordingly
        > on valid name entry check whether the filename already exists
        > create a filename in the notes table and 'filename'.txt file in the 'notes directory'
        > redirect to editor for document edit
    """

    # messagebox.()
    filename = simpledialog.askstring("New File","Enter new file name \n(NOTE: all files are by default .txt. Thankyou!)")
    print(filename)

    if filename == "":
        messagebox.showinfo("alert","please enter a valid name")
        create_new_file_window(current_user)
    if filename == None:
        pass
    else:
        if filename.isalnum():
            dbcursor.execute(f"SELECT * FROM notes WHERE filename = '{filename}'")# AND UID = '{current_user.UID}'")
            if dbcursor.fetchone():
                messagebox.showinfo("Alert","File already exists!!!")
                create_new_file_window(current_user)
            else:
                try:
                    dbcursor.execute(f"INSERT INTO notes(filename,UID) VALUES('{filename}','{current_user.UID}')")
                    connection.commit()
                    with open(os.path.join(os.getcwd(),"notes",filename+".txt"),"w") as f:
                        f.write(f"#created on {time.ctime()} by dhiraj yadav\n")
                except:
                    messagebox.showinfo("Error","some error occurred")
                else:
                    messagebox.showinfo("Success","file successfully created!!!")
                    note_editor(filename,current_user)
        else:
            messagebox.showinfo("Alert","only alphanumeric keys are valid filename!!!")
            create_new_file_window(current_user)

def note_editor(filename,current_user):
    """
        this is the editor window 
        > check whether the file name is correct or not
        > on correct:
            > open the file from the system
            > get the text from the file and insert it into the text box for editing
        > this window has three button SAVE (save the current changes), RESTORE(restore doc to last saved checkpoint) and CANCEL(open the notepad menu)
    """
    print("note-editor")
    if filename == "" or filename == None:
        messagebox.showinfo("Error","No file Chosen!!!")
    else:
        filename = filename + ".txt"
        try:
            textfile = open(os.path.join(os.getcwd(),"notes",filename),"r").read()
        except:
            messagebox.showinfo("Alert","File Does not exist on your home system!!!")
        else:
            # Editor Setup
            for widget in header.winfo_children():
                widget.destroy()
            numberline = Text(header,width=2,height=46,font=("Arial", 11,"bold"))
            numberline.insert(INSERT,"->\n"*50)
            numberline.config(state="disabled")
            editor = Text(header,width=193,height=46,font=("Arial", 11,"bold"))
            scrollbar = Scrollbar(header)
            scrollbar.pack(side=RIGHT,fill=Y,padx=0)
            numberline.pack(side=LEFT,padx=(6,1),pady=(6,7))
            editor.pack(side=LEFT,padx=(0,6),pady=(6,7))
            editor.config(yscrollcommand = scrollbar.set)
            numberline.config(yscrollcommand= scrollbar.set)
            scrollbar.config(command = editor.yview)
            editor.insert(INSERT,textfile)

            for widget in body.winfo_children():
                widget.destroy()

            save_file = Button(body,text = "SAVE",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: editor_save(editor.get("1.0",END),filename,current_user))
            save_file.pack(side=LEFT,pady=7,ipady=5,ipadx=4,padx=(1200,10))
            
            restore_file = Button(body,text = "RESTORE",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: editor_restore(filename,current_user))
            restore_file.pack(side=LEFT,pady=7,ipady=5,ipadx=5,padx=10)
            
            home_button = Button(body,text = "CANCEL",font=("Arial",12,"bold"),width=10,height = 1, bg = "#224",fg = "#fff",command = lambda: notepad(current_user))
            home_button.pack(side=LEFT,pady=7,ipady=7,ipadx=5,padx=10)

def editor_restore(filename,current_user):
    """
        this restore the data by simply reloading the file
    """
    note_editor(filename[:-4],current_user)

def editor_save(content,filename,current_user):
    """
        This methos the saves the changes bydirectly writing the contents from text box to the text file in the system ROM.
    """
    open(os.path.join(os.getcwd(),"notes",filename),"w").write(content)
    note_editor(filename[:-4],current_user)
    # pass
    

def notehome(email=None,password=None):
    """
    this method check if the user really exists.
    if true then redirect to notepad
    else show error message to the user
    """
    print("Arrived!!!")
    # print(email," ",password)
    dbcursor.execute("SELECT * from users WHERE email = '{}' AND passwd = '{}' ;".format(email,password))
    user_data = dbcursor.fetchone()
    if user_data:
        current_user = User(user_data)
        notepad(current_user)
    else:
        messagebox.showinfo("Alert","No such user exists!!!")

def login_tab_view(login_tab,register_tab):
    """
    this is the login view method contains all the definition for body of the login window
    > has two entry  for email and password
    > one login button to login which call the notehome function credentials verifications.
    """
    root.title("Login")
    login_tab["bg"] = body["bg"]
    register_tab["bg"] = "#666"
    for w in body.winfo_children():
        w.destroy()
    print("login")
    email_label = Label(body,text="Email: ",font=("Arial",10,"bold"),bg="#222",fg="#fff")
    email_label.pack(side=TOP,pady=(50,10),padx=100)
    email_entry = Entry(body,width = 100,text="enter email",font=("Arial",12,"bold"))
    email_entry.pack(side =TOP,pady=10,padx=50,ipadx=5,ipady=5)
    password_label = Label(body,text="Password: ",font=("Arial",10,"bold"),bg="#222",fg="#fff")
    password_label.pack(side=TOP,pady=10,padx=100)
    password_entry = Entry(body,width = 100,text="enter password",font=("Arial",12,"bold"))
    # password_entry.bind("<Return>",lambda: notehome(email_entry.get(),password_entry.get()))
    password_entry.pack(side=TOP,pady=10,padx=50,ipadx=5,ipady=5)
    log_me_in = Button(body,text="Login",font=("Arial",15,"bold"),width=30,height=2,bg="#0af",bd=0,fg="#fff",command =lambda: notehome(email_entry.get(),password_entry.get()))
    log_me_in.pack(side=TOP,padx=80,pady=(30,200),ipady=5)

def register(username,email,password):
    """
    this functions validates the user registration data.
    valid users are registered into the database
    and directly redirect to notepad
    """
    if " " in  username or " " in email:
        messagebox.showinfo("Warning","spaces are not allowed in username and email")

    dbcursor.execute("SELECT * from users where email = '{}'".format(email))
    data = dbcursor.fetchone()
    if data:
        messagebox.showinfo("Alert","User already exists try different username")
    else:
        dbcursor.execute("INSERT INTO users (name,email,passwd) VALUES('{}','{}','{}')".format(username,email,password))
        connection.commit()
        dbcursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
        current_user = User(dbcursor.fetchone())
        notepad(current_user)


def registration_tab_view(login_tab,register_tab):
    """
        this is the registration window. it contains:
        > 3 entry objects for : username, email, password
        > registration button which directly calls the register methods for credentials validations
    """
    global root
    global body
    global header
    login_tab["bg"] = "#666"
    register_tab["bg"] = body["bg"]
    root.title("Registration")
    for w in body.winfo_children():
        w.destroy()
    print("registration")
    username_label = Label(body,text="Name: ",font=("Arial",10,"bold"),bg="#222",fg="#fff")
    username_label.pack(side=TOP,pady=(50,5),padx=100)
    username_entry = Entry(body,width = 100,text="username",font=("Arial",12,"bold"))
    username_entry.pack(side =TOP,pady=10,padx=50,ipadx=5,ipady=5)
    email_label = Label(body,text="Email: ",font=("Arial",10,"bold"),bg="#222",fg="#fff")
    email_label.pack(side=TOP,pady=10,padx=100)
    email_entry = Entry(body,width = 100,text="enter email",font=("Arial",12,"bold"))
    email_entry.pack(side =TOP,pady=10,padx=50,ipadx=5,ipady=5)
    password_label = Label(body,text="Password: ",font=("Arial",10,"bold"),bg="#222",fg="#fff")
    password_label.pack(side=TOP,pady=10,padx=100)
    password_entry = Entry(body,width = 100,text="enter password",font=("Arial",12,"bold"))
    password_entry.pack(side=TOP,pady=10,padx=50,ipadx=5,ipady=5)
    register_me_in = Button(body,text="Register",font=("Arial",12,"bold"),width=30,height=2,bg="#0af",bd=0,fg="#fff",command =lambda: register(username_entry.get(),email_entry.get(),password_entry.get()))
    register_me_in.pack(side=TOP,padx=80,pady=(30,110))

root = Tk()
header = Frame(root)
header.pack(side=TOP)

body = Frame(root)
body.pack(side=TOP)

# login/registration
# current_user = User()
# notepad(current_user)
home()

root.mainloop()
