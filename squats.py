import tkinter as tk
import customtkinter as ctk
import numpy as np
import mediapipe as mp
import cv2
from PIL import Image, ImageTk

def handle_error(error_message):
    feedback_label.configure(text=error_message)

try:
    app = tk.Tk()
    app.geometry('640x700')
    app.title('Squat Page')
    app.resizable(False, False)

    def go_back():
        app.destroy()

    go_back_button = ctk.CTkButton(app, text="Go Back", command=go_back, height=40, width=120, text_color='white', fg_color='blue')
    go_back_button.place(x=10, y=650)

    class_label = ctk.CTkLabel(app, height=40, width=120, text_color='brown')
    class_label.place(x=10, y=1)
    class_label.configure(text='STAGE')

    counter_label = ctk.CTkLabel(app, height=40, width=120, text_color='brown')
    counter_label.place(x=160, y=1)
    counter_label.configure(text='REPS')

    class_box = ctk.CTkLabel(app, height=40, width=120, text_color='white', fg_color='blue')
    class_box.place(x=10, y=41)
    class_box.configure(text='')

    counter_box = ctk.CTkLabel(app, height=40, width=120, text_color='white', fg_color='blue')
    counter_box.place(x=160, y=41)
    counter_box.configure(text='0')

    feedback_label = ctk.CTkLabel(app, height=40, width=480, text_color='red', font=("Arial", 18))
    feedback_label.place(x=10, y=600)

    good_job_label = ctk.CTkLabel(app, height=40, width=480, text_color='green', font=("Arial", 18))
    good_job_label.place(x=10, y=570)

    def reset_counter():
        global rep_count
        rep_count = 0
        counter_box.configure(text=str(rep_count))
        feedback_label.configure(text='')
        current_stage = ''  # Reset stage

    reset_button = ctk.CTkButton(app, text='RESET', command=reset_counter, height=40, width=120, text_color='white', fg_color='blue')
    reset_button.place(x=250, y=650)

    frame = tk.Frame(app, width=640, height=480)
    frame.place(x=0, y=90)
    lmain = tk.Label(frame)
    lmain.place(x=0, y=0)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    rep_count = 0
    current_stage = ''  # Initialize current stage

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle

    def update_counter():
        global rep_count
        counter_box.configure(text=str(rep_count))

    def detect_squat(frame):
        global rep_count
        global current_stage

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            angle = calculate_angle(left_knee, [left_knee[0], left_knee[1] + 0.1], left_ankle)

            if angle > 150 and current_stage != "up":
                current_stage = "up"
            elif angle < 100 and current_stage != "down":
                current_stage = "down"
                rep_count += 1
                update_counter()
                if rep_count == 10:
                    good_job_label.configure(text='Congratulations! You completed 10 reps!')
                else:
                    feedback_label.configure(text='Well done! Keep going down with control and keep your back straight.')

                app.after(2000, lambda: feedback_label.configure(text=''))

            # Update stage box
            class_box.configure(text=current_stage.upper())

            # Draw angle on the frame
            cv2.putText(image, f'Angle: {angle:.2f}', (int(left_knee[0]), int(left_knee[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(106,13,173), thickness=4, circle_radius=5),
                mp_drawing.DrawingSpec(color=(255,102,0), thickness=5, circle_radius=10))

        return image

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            image = detect_squat(frame)
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
        lmain.after(10, update_frame)

    update_frame()
    app.mainloop()

except Exception as e:
    handle_error(f"An error occurred: {e}")