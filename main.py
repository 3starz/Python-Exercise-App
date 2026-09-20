from tkinter import *
from tkinter import messagebox, Toplevel, PhotoImage
import ast
import subprocess
import concurrent.futures
import customtkinter as ctk 
import pandas as pd
import numpy as np
import pickle
import mediapipe as mp
import cv2
from PIL import Image, ImageTk
from landmarks import landmarks
import datetime

# Function to open the Deadlift app
def open_deadlift_app():
    subprocess.run(["python", "deadlift.py"])

# Function to open the Deadlift app asynchronously
def open_deadlift_app_async():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(open_deadlift_app)

def open_squats_app():
    subprocess.run(["python", "squats.py"])

def open_squats_app_async():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(open_squats_app)

def signin():
    try:
        # Retrieve username and password from entry widgets
        username = user.get()
        password = code.get()

        # Read credentials from file or database
        with open('Datasheet.txt', 'r') as file:
            credentials = ast.literal_eval(file.read())

        # Check if username exists and password matches
        if username in credentials and credentials[username] == password:
            # Close the login window
            root.destroy()
            # Show the instructions page
            show_instructions_page()
        else:
            # Display error message for invalid credentials
            messagebox.showerror('Invalid', 'Invalid username or password')

    except Exception as e:
        print(f"Error in signin function: {e}")

def show_instructions_page():
    # Create a new window for the extra page
    extra_window = Tk()
    extra_window.title("Welcome")
    extra_window.geometry('600x400')
    extra_window.resizable(False,False)

    # Label for welcome message
    welcome_label = Label(extra_window, text="Welcome!", font=('Arial', 20))
    welcome_label.pack(pady=10)

    # Button to go to interface page and close the extra page
    interface_button = Button(extra_window, text="Go to Main Page", command=lambda: [extra_window.destroy(), interface_page()])
    interface_button.pack(pady=10)

    # Center the window
    center_window(extra_window)

    # Text widget for writing instructions
    instructions_text = Text(extra_window, wrap=WORD, height=10, state='normal')  # Set state to 'normal'
    instructions_text.pack(pady=10, padx=20, fill=BOTH, expand=True)

    instructions_text.insert(END, "Please read the instructions before proceeding:\n")
    instructions_text.insert(END, "1. This app is still in development.\n")
    instructions_text.insert(END, "2. Warm up for 5-6 minutes before starting the squats and deadlift before performing deadlifts and/or squats.\n")
    instructions_text.insert(END, "3. When you press the squats button or deadlift button, please wait a few seconds for the new window to open.\n")
    instructions_text.insert(END, "4. For the squats model, please do it sideways, and for deadlift, you may do it normally. \n")
    instructions_text.insert(END, "5. Make sure there are no people in the background when performing the exercises. \n")
    instructions_text.configure(state='disabled')  # Disable the text widget after inserting text


def settings_page():
    def change_theme(theme):
        if theme == "Light Theme":
            settings_window.configure(bg="white")
            if interface_window:
                interface_window.configure(bg="white")
        elif theme == "Dark Theme":
            settings_window.configure(bg="black")
            if interface_window:
                interface_window.configure(bg="black")
        elif theme == "Default Theme":
            settings_window.configure(bg="blue")
            if interface_window:
                interface_window.configure(bg="blue")

    def update_language(language):
        if language == "English":
            texts = english_texts
        elif language == "Spanish":
            texts = spanish_texts
        elif language == "French":
            texts = french_texts

        label.config(text=texts["Settings"])
        theme_label.config(text=texts["Theme"])
        language_label.config(text=texts["Language"])
        
        # Update radio buttons text
        for radio in theme_radios:
            radio.config(text=texts[radio["value"]])
        for radio in language_radios:
            radio.config(text=texts[radio["value"]])

    def change_language(language):
        # Placeholder for changing language
        print(f"Language changed to {language}")
        update_language(language)
    
    def submit_feedback(feedback_text, user_email, feedback_window):
        try:
            # Check if feedback text is empty
            if not feedback_text.strip():
                messagebox.showerror("Error", "Please enter feedback before submitting.")
                return

            # Save feedback to a file with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("feedback.txt", "a") as file:
                file.write(f"Timestamp: {timestamp}\n")
                file.write(f"User Email: {user_email}\n")
                file.write(f"Feedback: {feedback_text}\n\n")

            # Display confirmation message
            messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")

            # Close the feedback window
            feedback_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit feedback: {str(e)}")

    def open_feedback_window():
        # Create feedback window
        feedback_window = Toplevel(settings_window)
        feedback_window.title("Feedback")
        feedback_window.geometry("400x300")
        feedback_window.resizable(False, False)

        # Feedback text entry
        feedback_label = Label(feedback_window, text="Describe the issue:")
        feedback_label.pack()
        feedback_entry = Text(feedback_window, height=5)
        feedback_entry.pack()

        # Email entry (optional)
        email_label = Label(feedback_window, text="Your Email (optional):")
        email_label.pack()
        email_entry = Entry(feedback_window)
        email_entry.pack()

        # Submit button
        submit_button = Button(feedback_window, text="Submit", command=lambda: submit_feedback(feedback_entry.get("1.0", "end-1c"), email_entry.get(), feedback_window))
        submit_button.pack()

    # Translation dictionaries for text labels
    english_texts = {
        "Settings": "Settings",
        "Theme": "Theme:",
        "Light Theme": "Light Theme",
        "Dark Theme": "Dark Theme",
        "Default Theme": "Default Theme",
        "Language": "Language:",
        "English": "English",
        "Spanish": "Spanish",
        "French": "French",
        "Feedback": "Feedback",
        "Close":"Close"
    }

    spanish_texts = {
        "Settings": "Ajustes",
        "Theme": "Tema:",
        "Light Theme": "Tema Claro",
        "Dark Theme": "Tema Oscuro",
        "Default Theme": "Tema por Defecto",
        "Language": "Idioma:",
        "English": "Inglés",
        "Spanish": "Español",
        "French": "Francés",
    }

    french_texts = {
        "Settings": "Paramètres",
        "Theme": "Thème :",
        "Light Theme": "Thème Clair",
        "Dark Theme": "Thème Foncé",
        "Default Theme": "Thème par Défaut",
        "Language": "Langue :",
        "English": "Anglais",
        "Spanish": "Espagnol",
        "French": "Français",
    }

    # Create a new window for settings
    settings_window = Tk()
    settings_window.title("Settings")
    settings_window.geometry('400x400')
    settings_window.resizable(False, False)

    # Create a canvas
    canvas = Canvas(settings_window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a frame inside the canvas to hold the settings
    settings_frame = Frame(canvas)
    canvas.create_window((0, 0), window=settings_frame, anchor='nw')

    # Label for settings
    label = Label(settings_frame, text="Settings", font=('Arial', 18))
    label.pack(pady=20)

    # Theme settings
    theme_label = Label(settings_frame, text="Theme:")
    theme_label.pack(anchor='w')

    themes = ["Light Theme", "Dark Theme", "Default Theme"]
    theme_radios = []
    for theme in themes:
        theme_radio = Radiobutton(settings_frame, text=theme, value=theme, command=lambda t=theme: change_theme(t))
        theme_radio.pack(anchor='w')
        theme_radios.append(theme_radio)

    # Language settings
    language_label = Label(settings_frame, text="Language:")
    language_label.pack(anchor='w')

    languages = ["English", "Spanish", "French"]
    language_radios = []
    for language in languages:
        language_radio = Radiobutton(settings_frame, text=language, value=language, command=lambda l=language: change_language(l))
        language_radio.pack(anchor='w')
        language_radios.append(language_radio)

    # Feedback button
    feedback_button = Button(settings_frame, text="Feedback", command=open_feedback_window)
    feedback_button.pack(pady=10)

    # Close button
    close_button = Button(settings_frame, text="Close", command=settings_window.destroy)
    close_button.pack(pady=10)
    
    # Center the window
    center_window(settings_window)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Define interface_page function globally
def interface_page():
    global interface_window
    
    # Create a new window for the interface page
    interface_window = Tk()
    interface_window.title("Get started")
    interface_window.geometry('800x600')
    interface_window.configure(bg='blue')
    interface_window.resizable(False,False)

    # Create buttons for settings, squats, and deadlift
    settings_button = Button(interface_window, text="Settings", command=settings_page, height="4", width="10", bg="white", fg="black", font=("Arial", 20))
    settings_button.place(x=325, y=0)

    # Button for squats code
    squats_button = Button(interface_window, text="Squats", command=open_squats_app_async, height="4", width="10", bg="green", fg="white", font=("Arial", 20))
    squats_button.place(x=325, y=400)

    # Button for deadlift code
    deadlift_button = Button(interface_window, text="Deadlift", command=open_deadlift_app_async, height="4", width="10", bg="red", fg="white", font=("Arial", 20))
    deadlift_button.place(x=325, y=200)

    # Center the buttons horizontally
    interface_window.grid_columnconfigure(0, weight=1)

def signup_command():
    window=Toplevel(root)
    window.title("Signup")
    window.geometry('925x500+300+200')
    window.configure(bg='white')
    window.resizable(True,True)

    def signup():
        username=user.get()
        password=code.get()
        conform_password=conform_code.get()

        if password == conform_password:
            try:
                file=open('Datasheet.txt', 'r+')
                d=file.read()
                r=ast.literal_eval(d)

                dict2={username:password}
                r.update(dict2)
                file.truncate
                file.close()

                file=open('Datasheet.txt', 'w')
                w=file.write(str(r))

                messagebox.showinfo('Signup', 'Successfully sign up')
                window.destroy()

            except:
                file = open('Datasheet.txt', 'w')
                pp=str({'Username':'Password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invalid', "Both Password must match")

    def sign():
        window.destroy()

    img = PhotoImage(file='logi.png')
    Label(window,image=img,border=0,bg='white').place(x=50,y=90)

    frame=  Frame(window,width=350,height=390,bg='black')
    frame.place(x=1000,y=50)

    heading=Label(frame,text='Sign up',fg='blue', bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
    heading.place(x=120,y=5)

    def on_enter(e):
        code.delete(0,'end')
    def on_leave(e):
        if code.get()=='':
            code.insert(0,'Password')

    code= Entry(frame,width=25,fg='black',border=2,bg='white',font=('Microsoft Yahei UI Light',11), show='*')
    code.place(x=25,y=150)
    code.insert(0, 'Password')
    code.bind("<FocusIn>",on_enter)
    code.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get()=='':
            user.insert(0,'Username')

    user= Entry(frame,width=25,fg='black',border=2,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=25,y=83)
    user.insert(0, 'Username')
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=110)

    def on_enter(e):
        conform_code.delete(0,'end')
    def on_leave(e):
        if conform_code.get()=='':
            conform_code.insert(0,'Confirm Password')

    conform_code= Entry(frame,width=25,fg='black',border=2,bg='white',font=('Microsoft Yahei UI Light',11), show='*')
    conform_code.place(x=25,y=220)
    conform_code.insert(0, 'Confirm Password')
    conform_code.bind("<FocusIn>",on_enter)
    conform_code.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

    Button(frame,width=39,pady=7,text='Sign up',bg='White', fg='blue', border=0, command=signup).place(x=35,y=280)
    label=Label(frame,text='I have an account',fg='black',bg='red', font=('Microsoft Yahei UI Light', 9))
    label.place(x=90,y=340)

    signin=Button(frame,width=6,text='Sign in', border=0, bg='white', cursor='hand2', fg='blue',command=sign)
    signin.place(x=200,y=340)

    window.mainloop()

# Main window for login
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='Orange')
root.resizable(True, True)

# Logo image
img = PhotoImage(file='logi.png')
Label(root, image=img, bg='white').place(x=50, y=85)

# Frame for login
frame = Frame(root, width=500, height=500, bg='red')
frame.place(x=800, y=80)

# Heading for login
heading = Label(frame, text='Sign in', fg='Black', bg='white', font=('Microsoft YaHei UI light', 23, 'bold'))
heading.place(x=200, y=5)

# Function to handle focus events for entry fields
def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

def on_enter_password(e):
    code.delete(0, 'end')

def on_leave_password(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

# Entry fields for username and password
user = Entry(frame, width=25, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
user.place(x=10, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

code = Entry(frame, width=25, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11), show='*')
code.place(x=10, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_password)
code.bind('<FocusOut>', on_leave_password)

# Button for signing in
Button(frame, width=67, pady=7, text='Sign in', bg='blue', fg='white', border=0, command=signin).place(x=10, y=204)

# Label for sign up
Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9)).place(x=155, y=270)

# Button for sign up
Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='blue', command=signup_command).place(x=300, y=270)

root.mainloop()