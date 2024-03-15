import cv2
import numpy as np
import pyautogui

# Constants for red color detection
red_lower = np.array([0, 100, 100], dtype="uint8")
red_upper = np.array([10, 255, 255], dtype="uint8")

# Capture video stream from webcam
cap = cv2.VideoCapture(0)

# Initialize previous cursor position
prev_x, prev_y = 0, 0

while True:
    # Read frame from the video stream
    ret, frame = cap.read()

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only red color
    mask = cv2.inRange(hsv, red_lower, red_upper)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)

        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(max_contour)

        # Compute centroid of the detected red color region
        cx, cy = x + w // 2, y + h // 2

        # Move the cursor based on color detection
        pyautogui.moveTo(cx * 4, cy * 3)

        # Update previous cursor position
        prev_x, prev_y = cx * 4, cy * 3

    # Display the frame
    cv2.imshow('Red Color Cursor Control', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
