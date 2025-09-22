<img width="743" height="500" alt="image" src="https://github.com/user-attachments/assets/a02512b3-1a47-4977-82dc-a8976ee193f8" />



# OpenCV Getting Started (Python)

This tutorial shows the most common beginner operations in **cv2** with short code snippets.

---

## 1. Opening an Image
```python
import cv2

img = cv2.imread("image.jpg")   # loads in BGR format
```

---

## 2. Displaying the Image
```python
cv2.imshow("Original", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 3. Displaying the Shape (size)
```python
print("Shape:", img.shape)  # (height, width, channels)
```

---

## 4. Resizing
```python
resized = cv2.resize(img, (300, 200))  # width=300, height=200
cv2.imshow("Resized", resized)
cv2.waitKey(0)
```

---

## 5. Converting to Grayscale
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)
```

---

## 6. Drawing on the Image
```python
# Copy first
drawn = img.copy()

# Circle (center=(250,150), radius=50)
cv2.circle(drawn, (250,150), 50, (0,255,0), 2)

# Rectangle (top-left, bottom-right)
cv2.rectangle(drawn, (50,50), (200,200), (255,0,0), 2)

# Text
cv2.putText(drawn, "Hello OpenCV", (50, 300),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

cv2.imshow("Drawing", drawn)
cv2.waitKey(0)
```

---

## 7. Gaussian Blur
```python
blur = cv2.GaussianBlur(img, (7,7), 1)
cv2.imshow("Blur", blur)
cv2.waitKey(0)
```

---

## 8. Thresholding
```python
_, th = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
cv2.imshow("Threshold", th)
cv2.waitKey(0)
```

---

## 9. Canny Edge Detection
```python
edges = cv2.Canny(gray, 100, 200)
cv2.imshow("Canny Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---
