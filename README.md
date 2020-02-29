# note-editor
Python GUI app for editing and viewing text files

    LOGIN/ REGISTRATION
    HOME PAGE : Open doc / Create new doc / delete doc / logout
                Open : Show only that has been created
                    Save/ Cancel
                Create: ask for name of file check availability then save and open as edit
                    Save/ Cancel
                delete: Confirm on delete
                logout: Redirect to login/registration

## classes:
    - User:
        this class records the details of user which is currently active.
## methods:
    - home():
        this function is the home page of the app
        > resize the window and setup
        > clear the root window
        > add buttons for login and registration
        > call the login_view_tab to show login window

    - login_tab_view():
        this is the login view method contains all the definition for body of the login window
        > has two entry  for email and password
        > one login button to login which call the notehome function credentials verifications.

    - notehome():
        this method check if the user really exists.
        if true then redirect to notepad
        else show error message to the user

    - register_tab_view():
        this is the registration window. it contains:
        > 3 entry objects for : username, email, password
        > registration button which directly calls the register methods for credentials validations
   

    - register():
        this functions validates the user registration data.
        valid users are registered into the database
        and directly redirect to notepad


    - notepad():
        this window is after login:
         > destroy the header frame which previously contained login and registration button
         > destroy body
         > resize window and few tweaks to the window
         > fetch all the text files from the database associated with the user
         > check if there is any files created and act accordingly
         > if there are files associated with the user create a listbox to show it
         > add create , open , delete and logout button

    - delete_data():
        this function takes in two arguments current user and filename to be deleted.
        > check if there is something selected or just a prank
        > if there is then delete the filename from notes table in the database
        > then use shutil to move the file from 'notes' folder to 'deleted' folder == because we dont lose data.

    - create_new_file():
        this window creates a new file in the user system
        > ask for the filename through a dialog box
        > handle errors accordingly
        > on valid name entry check whether the filename already exists
        > create a filename in the notes table and 'filename'.txt file in the 'notes directory'
        > redirect to editor for document edit

    - note_editor():
        this is the editor window 
        > check whether the file name is correct or not
        > on correct:
            > open the file from the system
            > get the text from the file and insert it into the text box for editing
        > this window has three button SAVE (save the current changes), RESTORE(restore doc to last saved checkpoint) and CANCEL(open the notepad menu)
    
    - editor_restore():
        this restore the data by simply reloading the file

    - editor_save():
        This methos the saves the changes bydirectly writing the contents from text box to the text file in the system ROM.
