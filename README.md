# Eye Tracking Alarm System (Ramiz Dayi Wake Up)

This project performs real-time eye tracking via a web camera using the **OpenCV** and **MediaPipe** libraries. When the user keeps their eyes closed for a specified duration (default is 5 seconds), it automatically plays a local video file (such as the Ramiz Dayi alarm video).

## 🚀 Features

* **Real-Time Eye Tracking:** Accurately detects facial landmarks and the vertical distance of the eyelids using MediaPipe Face Mesh.
* **Countdown Mechanism:** Displays a dynamic countdown timer on the screen showing the remaining time while eyes are kept closed.
* **Automatic Media Playback:** Once the condition is met (`5 seconds`), the script breaks the loop and launches the target video file using the default media player.
* **User-Friendly Interface:** Shows instant status notifications on the screen (`Close your eyes!` / `Eyes Closed! Remaining: X s`).

## 📋 Requirements

Python must be installed on your system before running the project. You can install the required libraries by running the following command in your terminal:

```bash
pip install opencv-python mediapipe
