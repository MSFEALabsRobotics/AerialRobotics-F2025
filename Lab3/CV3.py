import cv2
import numpy as np


# # #TAKING OFF
# SimulationRev3.arm_drone()
# SimulationRev3.get_barometer_data()
# SimulationRev3.takeoff(10)  # Takeoff to 10 meters altitude
# SimulationRev3.get_barometer_data()


# Callback function for the trackbar
def nothing(x):
    pass


# Create a window
cv2.namedWindow('TR Image')
# Resize the window to 256x256
cv2.resizeWindow('TR Image', 256, 256)

# Create a trackbar in the window for adjusting the threshold value (0 to 255)
cv2.createTrackbar('Bar1', 'TR Image', 0, 255, nothing)
cv2.createTrackbar('Bar2', 'TR Image', 0, 255, nothing)
cv2.createTrackbar('Bar3', 'TR Image', 0, 255, nothing)
cv2.createTrackbar('Bar4', 'TR Image', 0, 255, nothing)
cv2.createTrackbar('Bar5', 'TR Image', 0, 255, nothing)
cv2.createTrackbar('Bar6', 'TR Image', 0, 255, nothing)



while True:

        # Get the current value of the trackbar
    VAL1 = cv2.getTrackbarPos('Bar1', 'TR Image')
    VAL2 = cv2.getTrackbarPos('Bar2', 'TR Image')
    VAL3 = cv2.getTrackbarPos('Bar3', 'TR Image')
    VAL4 = cv2.getTrackbarPos('Bar4', 'TR Image')
    VAL5 = cv2.getTrackbarPos('Bar5', 'TR Image')
    VAL6 = cv2.getTrackbarPos('Bar6', 'TR Image')


    img = None
  


    # Convert the image to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the color range for detecting red (in HSV)
    # Define the range for the orange color in HSV
    lower_orange = np.array([VAL1, VAL2, VAL3])
    upper_orange = np.array([VAL4, VAL5, VAL6])

    # Create a mask for red color
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    cv2.imshow('Red Mask', mask)
 
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print(mask.shape)

    # Apply the mask to the original image (bitwise AND)
    result = cv2.bitwise_and(rgb, rgb, mask=mask)
    cv2.imshow('Red Detection Result', result)
    cv2.waitKey(1)
    # cv2.destroyAllWindows()



