# import cv2
# import mediapipe as mp

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands()

# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         break

#     # Convert the BGR image to RGB and process it with MediaPipe Hands.
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image.flags.writeable = False
#     results = hands.process(image)

#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#     # Display the resulting frame
#     cv2.imshow('MediaPipe Hands', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp

# Create a VideoCapture object
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Initialize the hand detection model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the BGR image to RGB before processing
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and draw the hand landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # thumb_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y
            # index_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            # middle_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            # ring_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
            # pinky_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y
            # print(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y)
            # print(thumb_is_open)
            # print(index_is_open)
            thumb_is_open1 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_is_open2 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_DIP]
            thumb_is_open3 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_PIP]
            thumb_is_open4 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

            index_is_open1 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_is_open2 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
            index_is_open3 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            index_is_open4 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            middle_is_open1 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_is_open2 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
            middle_is_open3 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            middle_is_open4 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            ring_is_open1 = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_is_open2 = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
            ring_is_open3 = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            ring_is_open4 = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]

            pinky_is_open1 = hand_landmarks.landmark[mp_hands.HandLandmark.HandLandmark.PINKY_TIP]
            pinky_is_open2 = hand_landmarks.landmark[mp_hands.HandLandmark.HandLandmark.PINKY_DIP]
            pinky_is_open3 = hand_landmarks.landmark[mp_hands.HandLandmark.HandLandmark.PINKY_PIP]
            pinky_is_open4 = hand_landmarks.landmark[mp_hands.HandLandmark.HandLandmark.PINKY_MCP]

            # print(chee1,chee2,chee3,chee4)

            print(thumb_is_open1)
            print(thumb_is_open2)
            print(thumb_is_open3)
            print(thumb_is_open4)
            
            print(index_is_open1)
            print(index_is_open2)
            print(index_is_open3)
            print(index_is_open4)

            print(middle_is_open1)
            print(middle_is_open2)
            print(middle_is_open3)
            print(middle_is_open4)

            print(ring_is_open1)
            print(ring_is_open2)
            print(ring_is_open3)
            print(ring_is_open4)

            print(pinky_is_open1)
            print(pinky_is_open2)
            print(pinky_is_open3)
            print(pinky_is_open4)
            # print(thumb_is_open1.x)
            # fingers_open = thumb_is_open + index_is_open + middle_is_open + ring_is_open + pinky_is_open
            # print(f'Fingers open: {fingers_open}')

            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the capture object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
