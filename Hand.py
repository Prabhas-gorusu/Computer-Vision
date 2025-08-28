import cv2
import mediapipe as mp
import time
import math
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Calculator buttons layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "C", "=", "+"]
]

# Smaller button size
button_w, button_h = 60, 60
button_spacing = 10

# Calculator frame size
frame_w = 4 * button_w + 5 * button_spacing
frame_h = 4 * button_h + 5 * button_spacing + 100  # extra space for input/output

# Pinch thresholds
number_threshold = 35
operation_threshold = 25

# Calculator state
current_input = ""
result = ""
last_click_time = 0
click_delay = 0.5
pressed_button = None

cap = cv2.VideoCapture(0)
tip_ids = [4, 8, 12, 16, 20]

# Fixed position: right-top corner
ret, frame = cap.read()
cam_h, cam_w, _ = frame.shape
offset_x = cam_w - frame_w - 20
offset_y = 20

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def draw_transparent_rect(frame, x, y, w, h, color=(50,50,50), alpha=0.5, border_thick=2):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x+w, y+h), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,0), border_thick)

def draw_buttons(frame, hover=None, hover_type=None, press=None):
    for i,row in enumerate(buttons):
        for j,val in enumerate(row):
            x = offset_x + button_spacing + j*(button_w + button_spacing)
            y = offset_y + 60 + button_spacing + i*(button_h + button_spacing)
            btn_color = (70,70,70)
            if hover == (i,j):
                btn_color = (0,255,0) if hover_type=="number" else (0,165,255)
            # Transparent button
            overlay = frame.copy()
            cv2.rectangle(overlay, (x, y), (x+button_w, y+button_h), btn_color, -1)
            alpha_btn = 0.6
            cv2.addWeighted(overlay, alpha_btn, frame, 1-alpha_btn, 0, frame)
            cv2.rectangle(frame, (x, y), (x+button_w, y+button_h), (0,0,0), 2)
            # Pressed effect
            if press == (i,j):
                cv2.rectangle(frame, (x+5, y+5), (x+button_w-5, y+button_h-5), (50,50,50), -1)
                cv2.rectangle(frame, (x+5, y+5), (x+button_w-5, y+button_h-5), (0,0,0), 2)
            cv2.putText(frame, val, (x+15, y+35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

def check_hover(finger_x, finger_y):
    for i,row in enumerate(buttons):
        for j,val in enumerate(row):
            x = offset_x + button_spacing + j*(button_w + button_spacing)
            y = offset_y + 60 + button_spacing + i*(button_h + button_spacing)
            if x < finger_x < x+button_w and y < finger_y < y+button_h:
                return i,j,val
    return None,None,None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_mp = hands.process(rgb_frame)

    hover_button = None
    hover_type = None
    pressed_button = None

    # Transparent calculator frame
    draw_transparent_rect(frame, offset_x, offset_y, frame_w, frame_h, color=(50,50,50), alpha=0.4, border_thick=2)

    if result_mp.multi_hand_landmarks:
        hand_landmarks = result_mp.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        tx, ty = int(thumb_tip.x*w), int(thumb_tip.y*h)
        ix, iy = int(index_tip.x*w), int(index_tip.y*h)

        cv2.circle(frame, (tx,ty), 7, (0,0,255), -1)
        cv2.circle(frame, (ix,iy), 7, (0,255,0), -1)
        cv2.line(frame, (tx,ty),(ix,iy),(255,255,0),2)

        # Hover and pinch detection
        i,j,val = check_hover(ix,iy)
        if i is not None:
            hover_button = (i,j)
            hover_type = "number" if val in "0123456789" else "operation"
            pinch_distance = math.hypot(tx-ix, ty-iy)

            if val in "0123456789" and pinch_distance < number_threshold:
                pressed_button = (i,j)
            elif val in "+-*/=C" and pinch_distance < operation_threshold:
                pressed_button = (i,j)

            # Register click
            if time.time()-last_click_time > click_delay:
                if val in "0123456789" and pinch_distance < number_threshold:
                    current_input += val
                    last_click_time = time.time()
                elif val in "+-*/=C" and pinch_distance < operation_threshold:
                    if val=="C":
                        current_input=""
                        result=""
                    elif val=="=":
                        try:
                            result=str(eval(current_input))
                        except:
                            result="Error"
                        current_input=""
                    else:
                        current_input += val
                    last_click_time = time.time()

    draw_buttons(frame, hover=hover_button, hover_type=hover_type, press=pressed_button)

    cv2.putText(frame, f"Input: {current_input}", (offset_x + 15, offset_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(frame, f"Result: {result}", (offset_x + 15, offset_y + 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Hand Calculator", frame)
    key = cv2.waitKey(1)
    if key==27 or key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
