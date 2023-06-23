# import cv2
# from cvzone.HandTrackingModule import HandDetector

# cap = cv2.imgeoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# detector = HandDetector(detectionCon=0.6, maxHands= 2)

# while True:
#   _, img = cap.read()

#   hands, img = detector.findHands(img)
#   cv2.imshow("Smart Camera",img)
#   if cv2.waitKey(1) == ord("q"):
#     break
# # After the loop release the cap object
# cap.release()
# # Destroy all the windows
# cv2.destroyAllWindows()
# import the opencv library
# This code is capturing imgeo from the default camera of the device and displaying it in a window
# using the OpenCV library. It also allows the user to quit the window by pressing the 'q' key. The
# lines `cap.set(3, 1280)` and `cap.set(4, 720)` set the resolution of the imgeo capture to 1280x720.
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)
while(True):
	
	ret, frame = cap.read()
	cv2.imshow('frame', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
