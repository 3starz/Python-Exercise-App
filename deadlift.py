import tkinter as tk
import customtkinter as ctk
import pandas as pd
import numpy as np
import pickle
import mediapipe as mp
import cv2
from PIL import Image, ImageTk
from landmarks import landmarks

def handle_error(error_message):
    feedback_label.configure(text=error_message)

try:
    app = tk.Tk()
    app.geometry('480x700')
    app.title('Deadlift Page')
    app.resizable(False,False)

    def go_back():
        app.destroy()

    go_back_button = ctk.CTkButton(app, text="Go Back", command=go_back, height=40, width=120, text_color='white', fg_color='blue')
    go_back_button.place(x=10, y =650)

    class_label = ctk.CTkLabel(app, height=40, width=120, text_color='black')
    class_label.place(x=10, y=1)
    class_label.configure(text='STAGE')

    counter_label = ctk.CTkLabel(app, height=40, width=120, text_color='black')
    counter_label.place(x=160, y=1)
    counter_label.configure(text='REPS')

    class_box = ctk.CTkLabel(app, height=40, width=120, text_color='white', fg_color='black')
    class_box.place(x=10, y=41)
    class_box.configure(text='0')

    counter_box = ctk.CTkLabel(app, height=40, width=120, text_color='white', fg_color='black')
    counter_box.place(x=160, y=41)
    counter_box.configure(text='0')

    feedback_label = ctk.CTkLabel(app, height=40, width=480, text_color='red', font=("Arial", 18))
    feedback_label.place(x=10, y=600)

    good_job_label = ctk.CTkLabel(app, height=40, width=480, text_color='green', font=("Arial", 18))
    good_job_label.place(x=10, y=570)

    def reset_counter():
        global counter
        counter = 0
        feedback_label.configure(text='')

    button = ctk.CTkButton(app, text='RESET', command=reset_counter, height=40, width=120, text_color='white', fg_color='blue')
    button.place(x=250, y=650)

    frame = tk.Frame(height=480, width=480)
    frame.place(x=10, y=90)
    lmain = tk.Label(frame)
    lmain.place(x=0, y=0)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

    with open('deadlift.pkl', 'rb') as f:
        model = pickle.load(f)

    cap = cv2.VideoCapture(0)
    current_stage = ''
    counter = 0

    body_lang_prob = np.array([0, 0])
    body_lang_class = ''

    def detect():
        global current_stage
        global counter
        global body_lang_class
        global body_lang_prob

        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(106,13,173), thickness=4, circle_radius=5),
                mp_drawing.DrawingSpec(color=(255,102,0), thickness=5, circle_radius=10))

            try:
                row = np.array([[res.x, res.y, res.z, res.visibility] for res in result.pose_landmarks.landmark]).flatten().tolist()
                x = pd.DataFrame([row], columns=landmarks)
                bodylang_prob = model.predict_proba(x)[0]
                bodylang_class = model.predict(x)[0]

                if current_stage == "down" and bodylang_class == "down" and bodylang_prob[bodylang_prob.argmax()] > 0.67:
                    # Provide feedback when the user is in the "down" position and should start going "up"
                    feedback_label.configure(text='Start going up.')

                elif current_stage == "down" and bodylang_class == "up" and bodylang_prob[bodylang_prob.argmax()] > 0.7:
                    current_stage = "up"
                    counter += 1
                    feedback_label.configure(text='')  # Clear feedback when correct

                    # Display "Well done!" message
                    good_job_label.configure(text='Well done! Go up with a straight back.')

                    # Reset the message after a short delay
                    app.after(2000, lambda: good_job_label.configure(text=''))

                elif bodylang_class == "down" and bodylang_prob[bodylang_prob.argmax()] > 0.7:
                    current_stage = "down"
                    feedback_label.configure(text='Keep going down. Maintain a straight back.')

                else:
                    feedback_label.configure(text='')

                    feedback_label.configure(text='Check your posture at all times. Keep your back straight.')

            except Exception as e:
                print(e)
        else:
            # Clear feedback when no pose landmarks are detected
            feedback_label.configure(text='')

        img = image[:, :460, :]
        imgarr = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(imgarr)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, detect)

        counter_box.configure(text=counter)
        class_box.configure(text=current_stage)

    detect()

    app.mainloop()

except Exception as e:
    handle_error(f"An error occurred: {e}")