# Exercise App

A Python desktop app that uses your webcam and pose estimation (MediaPipe) to count repetitions and give live feedback while you do **squats** and **deadlifts**. It includes a login and sign-up system, an instructions page, a settings menu and an in-app feedback form.

<img width="1919" height="1013" alt="Screenshot 2024-03-31 180910" src="https://github.com/user-attachments/assets/31552254-b4d9-443f-b6b2-e8e13644b890" />
<img width="649" height="880" alt="Screenshot 2024-03-31 024011" src="https://github.com/user-attachments/assets/54caae5d-cc71-4d84-b51f-54790100f536" />
<img width="587" height="829" alt="Screenshot 2024-03-29 004956" src="https://github.com/user-attachments/assets/4b810acc-a167-4376-b0f9-dfa014bac389" />


## Features

- **Pose estimation:** tracks 33 body landmarks from the webcam in real time using MediaPipe
- **Squats:** calculates the knee angle from the landmarks to detect the "up" and "down" stages, counts reps and shows feedback (with a congratulations message at 10 reps)
- **Deadlifts:** a pre-trained scikit-learn classifier takes the body landmarks and predicts whether you are in the "up" or "down" stage. Reps are counted on a full down-to-up movement, and on-screen messages remind you to keep your back straight
- **Login and sign-up:** Tkinter screens with password confirmation and error messages for invalid details
- **Settings:** theme and language options, plus a feedback form that saves reports to a file
- **Instructions page** with tips for getting accurate results

## Built with

- Python
- MediaPipe and OpenCV (pose estimation and webcam capture)
- scikit-learn, pandas and NumPy (deadlift stage classifier)
- Tkinter, CustomTkinter and Pillow (user interface)

## Getting started

### Requirements

- Python 3.10 recommended (the deadlift model was saved with scikit-learn 1.1.2, which needs an older Python)
- A webcam

### Installation

```bash
git clone https://github.com/YOUR-USERNAME/exercise-app.git
cd exercise-app
pip install -r requirements.txt
```

### Run the app

python main.py

Sign up, log in, read the instructions page, then choose **Squats** or **Deadlift**. You can also run `squats.py` or `deadlift.py` directly to skip the menus.

## Tips for best results

- Warm up before exercising
- Wait a few seconds after pressing Squats or Deadlift for the camera window to open
- For squats, stand **sideways** to the camera. Deadlifts can be filmed normally
- Make sure nobody else is in the background, and keep your whole body in frame

## How it works

1. The webcam feed is read with OpenCV and passed frame by frame to MediaPipe Pose, which returns 33 body landmarks (x, y, z and visibility).
2. **Squats:** the app calculates a knee angle from the landmarks. Above a set angle counts as "up", below a set angle as "down", and each down movement adds one rep.
3. **Deadlifts:** the 132 landmark values (33 landmarks x 4) are fed to a pre-trained Random Forest model, which predicts "up" or "down" with a confidence score. The app only acts on predictions above a confidence threshold, which reduces false counts.
4. Feedback messages, the current stage and the rep count are shown in the interface.

## Testing and feedback

The app has a built-in feedback form. Early testers reported occasional crashes, so stability under different cameras and lighting is something I'd improve next.

## Known limitations

- **Passwords are stored in plain text** in a local file. This is a learning project and not secure enough for real use
- Squat detection uses the left knee only, so camera angle and lighting affect accuracy
- The deadlift model is pre-trained and not tuned to individual users or camera setups
- The squat and deadlift pages open as separate windows

## Ideas for improvement

- Hash passwords (for example with `bcrypt`) or use a proper database
- Use a hip-knee-ankle angle for squats and check both legs
- Train my own deadlift model on recordings of my own
- Save workout history and progress over time
- Add more exercises and voice feedback

## Acknowledgements

This project builds on tutorials and open-source libraries:

- [MediaPipe](https://developers.google.com/mediapipe) by Google for pose estimation
- The pre-trained deadlift classifier (`deadlift.pkl`) and the landmark-based approach come from **[
I tried to build a Machine Learning Python App in 15 Minutes | Coding Challenge]** by **[Nicholas Renotte]** ([(https://www.youtube.com/watch?v=zaBy3X37Oa8)])

My own work was integrating these into one app, building the main menu, instructions page, settings and feedback form, adding the login and sign-up system with validation, writing the squat rep counter, and testing with users.

## Author

Abdul Haseeb, BSc Computer Science student at Birkbeck, University of London
