#PART1: TRACK BARS USAGE WITH THRESHOLDING

import cv2
import numpy as np

# Callback function for the trackbar
def nothing(x):
    pass

# Load an image (you can change the path to your own image)
image = cv2.imread('output.jpg', cv2.IMREAD_GRAYSCALE)  # Convert to grayscale for thresholding

# Create a window
cv2.namedWindow('Threshold Image')

# Create a trackbar in the window for adjusting the threshold value (0 to 255)
cv2.createTrackbar('Threshold', 'Threshold Image', 0, 255, nothing)


while True:
    
    # Get the current value of the trackbar
    threshold_value = cv2.getTrackbarPos('Threshold', 'Threshold Image')
    
    # Apply the binary threshold
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Display the thresholded binary image
    cv2.imshow('Threshold Image', binary_image)
    
    # Wait for key press, break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Clean up and close windows
cv2.destroyAllWindows()




#PART2: FINDING CONTOURS BASED ON COLOR DETECTION MASK

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range for the orange color in HSV
lower_orange = np.array([5, 150, 150])
upper_orange = np.array([15, 255, 255])

# Create a binary mask where orange colors are white and the rest are black
mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
