🖐️ Hand Gesture Controlled Calculator

A virtual calculator controlled using hand gestures via a webcam, built with OpenCV and MediaPipe.
This project allows you to perform basic arithmetic operations (+, -, *, /) by pinching your thumb and index finger over calculator buttons displayed on the screen.


✨ Features

👆 Hover over calculator buttons using your index finger.

🤏 Pinch gesture (thumb + index finger) to press a button.

🔢 Supports digits 0-9 and operations +, -, *, /.

✅ Includes C (Clear) and = (Evaluate) functions.

🎨 Interactive UI with transparent buttons and pressed effects.

🖼️ Calculator frame is fixed at the top-right corner of the webcam feed.




🛠️ Tech Stack

Python 3.x

OpenCV – for computer vision & UI rendering

MediaPipe Hands – for real-time hand landmark detection

NumPy – numerical operations

Math & Time modules – distance calculation and click delay handling




📂 Project Structure

Hand-Calculator/
│── hand_calculator.py   # Main source code
│── README.md            # Project documentation



▶️ How to Run

1. Clone the repository

git clone https://github.com/prabhas-gorusu/Computer-Vision.git

cd Computer-Vision

2. Install dependencies

pip install opencv-python mediapipe numpy

3. Run the script

python hand_calculator.py



🎮 Controls

Hover → Move your index finger over a button.

Press → Pinch (bring thumb & index finger together).

Clear (C) → Erases current input and result.

Equal (=) → Evaluates the entered expression.

Exit → Press q or Esc.




📸 Demo (Concept)

> (Replace this with your screenshot or demo GIF)






🚀 Future Improvements

Add decimal support.

Add scientific functions (√, %, sin, cos, etc.).

Improve gesture recognition (multi-finger support).

Add voice feedback for pressed keys.




📜 License

This project is licensed under the MIT License – feel free to use and modify.


