import tkinter as tk
import customtkinter as ctk
import pandas as pd
import numpy as np
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

    def calculate_angle(a, b, c):
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
    
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
    
            if angle > 180.0:
                angle = 360-angle
    
            return angle

    button = ctk.CTkButton(app, text='RESET', command=reset_counter, height=40, width=120, text_color='white', fg_color='blue')
    button.place(x=250, y=650)

    frame = tk.Frame(height=480, width=480)
    frame.place(x=10, y=90)
    lmain = tk.Label(frame)
    lmain.place(x=0, y=0)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

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
            pose_landmarks = result.pose_landmarks.landmark

            # Deadlifts are identified from the hip hinge.
            # The hip angle is shoulder -> hip -> knee.
            left_shoulder = [pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [pose_landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         pose_landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            angle = calculate_angle(left_shoulder, left_hip, left_knee)

            # Tune these two values if your displayed angles differ slightly.
            if angle > 160 and current_stage != "up":
                current_stage = "up"
            elif angle < 115 and current_stage != "down":
                current_stage = "down"
                counter += 1
                if counter == 10:
                    good_job_label.configure(text='Congratulations! You completed 10 reps!')
                else:
                    feedback_label.configure(text='Well done! Keep your back straight and hinge at the hips.')

                app.after(2000, lambda: feedback_label.configure(text=''))

            # Update stage box
            class_box.configure(text=current_stage.upper())

            # Draw hip angle on the frame
            cv2.putText(image, f'Hip angle: {angle:.2f}',
                        (int(left_hip[0] * 460), int(left_hip[1] * 480) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(106,13,173), thickness=4, circle_radius=5),
                mp_drawing.DrawingSpec(color=(255,102,0), thickness=5, circle_radius=10))

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
