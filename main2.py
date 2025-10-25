import cv2
import mediapipe as mp
import pyautogui

# --- Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# --- Captura desde la cámara
cap = cv2.VideoCapture(0)
prev_x, prev_y = None, None
umbral = 60
screen_width, screen_height = pyautogui.size()

def get_landmark_coords(landmarks, index):
    lm = landmarks.landmark[index]
    return lm.x, lm.y

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_side = results.multi_handedness[idx].classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            ix, iy = get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)

            if hand_side == 'Right':
                mx, my = get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_MCP)
                tx, ty = get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP)

                # Calcular la distancia entre el índice y el pulgar
                distance = ((ix - tx)**2 + (iy - ty)**2) ** 0.5
                if distance < 0.05:
                    pyautogui.click()

                cursor_x = int(mx * screen_width)
                cursor_y = int(my * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

            elif hand_side == 'Left':
                x, y = int(ix * screen_width), int(iy * screen_height)
                if prev_x is not None and prev_y is not None:
                    dx, dy = x - prev_x, y - prev_y

                    if abs(dx) > abs(dy):
                        if dx > umbral:
                            pyautogui.press('right')
                        elif dx < -umbral:
                            pyautogui.press('left')
                    else:
                        if dy > umbral:
                            pyautogui.press('down')
                        elif dy < -umbral:
                            pyautogui.press('up')

                prev_x, prev_y = x, y

    cv2.imshow("Captura de gestos", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
