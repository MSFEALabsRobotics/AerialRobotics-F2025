# OpenCV Tutorial: Canny Edge Detection & Contours (Python)
_A compact, practical guide with runnable code._

> **Prereqs**
> ```bash
> pip install opencv-python numpy
> ```
> Put an image named `image.jpg` in the same folder **or** rely on the script’s built‑in synthetic demo image.

---

## 1) Quick concepts (what & why)
- **Canny edge detection** finds intensity changes (edges) using gradient + non‑max suppression + hysteresis thresholds. Great as a first step before finding shapes.
- **Contours** are curves joining continuous points along a boundary. If you can get a clean edge map (from Canny or thresholding), you can extract objects, measure areas, draw bounding boxes, etc.

---

## 2) Minimal end‑to‑end example
Copy this into a file (e.g., `contours_canny_demo.py`) and run:
```python
import cv2
import numpy as np

# ---------- Load or synthesize a demo image ----------
img = cv2.imread('image.jpg')  # BGR
if img is None:
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.putText(img, 'Demo', (220, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255,255,255), 3, cv2.LINE_AA)
    cv2.rectangle(img, (80, 150), (250, 320), (255,255,255), -1)   # white rect
    cv2.circle(img, (420, 260), 70, (255,255,255), -1)             # white circle

# ---------- Preprocess ----------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Light blur helps denoise before Canny/threshold
blur = cv2.GaussianBlur(gray, (5, 5), 1.0)

# ---------- Option A: Canny edges ----------
# Two thresholds (lower, upper). Tune for your image.
edges = cv2.Canny(blur, threshold1=80, threshold2=160)

# ---------- Option B: Binary threshold (alternative to Canny) ----------
# _, binary = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)    # try simple
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)  # auto Otsu

# ---------- Find contours ----------
# You can use 'edges' OR 'binary'. Try both to see which is cleaner.
contour_src = edges  # change to 'binary' to compare
contours, hierarchy = cv2.findContours(contour_src, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"Found {len(contours)} contours")

# ---------- Draw results ----------
out = img.copy()
cv2.drawContours(out, contours, -1, (0, 255, 0), 2)

# ---------- Measure each contour ----------
for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    x,y,w,h = cv2.boundingRect(c)
    (cx, cy), radius = cv2.minEnclosingCircle(c)

    # Approximate polygon (e.g., to detect triangles/rectangles)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)
    n_verts = len(approx)

    # Filter tiny noise
    if area < 100:
        continue

    # Draw bounding box & label
    cv2.rectangle(out, (x,y), (x+w, y+h), (255, 0, 0), 2)
    label = f"#{i}: A={int(area)} P={int(peri)} V={n_verts}"
    cv2.putText(out, label, (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1, cv2.LINE_AA)
    # Center marker
    cv2.circle(out, (int(cx), int(cy)), 3, (0,0,255), -1)

# ---------- Show ----------
cv2.imshow('Original', img)
cv2.imshow('Blur', blur)
cv2.imshow('Canny edges', edges)
cv2.imshow('Binary (Otsu)', binary)
cv2.imshow('Contours overlay', out)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ---------- Save outputs ----------
cv2.imwrite('edges.png', edges)
cv2.imwrite('binary.png', binary)
cv2.imwrite('contours_overlay.png', out)
print('Saved: edges.png, binary.png, contours_overlay.png')
```

**What to tweak first:** `threshold1`, `threshold2` (Canny) and the blur size/sigma. For thresholding, try changing from `Otsu` to a fixed value (e.g., `120`) if lighting is stable.

---

## 3) Understanding Canny parameters
```python
edges = cv2.Canny(blur, threshold1=80, threshold2=160, L2gradient=True)
```
- `threshold1` (lower) and `threshold2` (upper) set hysteresis bands. If edges are broken, lower them; if noise explodes, raise them.
- `L2gradient=True` uses a more accurate gradient magnitude (Euclidean). Slightly slower but often cleaner.

**Tip:** A common starting point is `threshold2 ≈ 2 × threshold1`. Scale both up/down with image contrast/noise.

---

## 4) Choosing retrieval mode & approximation
```python
contours, hierarchy = cv2.findContours(src, mode, method)
```
- **mode**:
  - `cv2.RETR_EXTERNAL` → only outer contours (ignores holes). Great for object counting.
  - `cv2.RETR_TREE` → full hierarchy (outer/inner). Needed if holes matter (e.g., donut shapes).
- **method**:
  - `cv2.CHAIN_APPROX_SIMPLE` → compresses horizontal/vertical points (lighter, typical).
  - `cv2.CHAIN_APPROX_NONE` → keeps all points (heavy, rarely needed).

---

## 5) Filtering & classifying shapes
```python
area = cv2.contourArea(c)
peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.02*peri, True)
n_verts = len(approx)

if area < 100:    # noise filter
    continue

if n_verts == 3:  shape = 'triangle'
elif n_verts == 4:
    x,y,w,h = cv2.boundingRect(approx)
    ratio = w/float(h)
    shape = 'square' if 0.90 <= ratio <= 1.10 else 'rectangle'
elif n_verts > 8: shape = 'circle-ish'
else:             shape = f'{n_verts}-gon'
```
Adjust the `0.02*peri` epsilon: smaller = tighter fit (more vertices), larger = looser fit (fewer vertices).

---

## 6) Handling holes (hierarchy)
Use `cv2.RETR_TREE` and the `hierarchy` array to tell parents from children (holes). Example:
```python
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# hierarchy shape: (1, N, 4) => [Next, Prev, FirstChild, Parent] indices
for i, c in enumerate(contours):
    parent = hierarchy[0][i][3]
    if parent != -1:
        # This contour is a hole inside contour 'parent'
        pass
```

---

## 7) Common pitfalls & fixes
- **Edges missing?** Increase contrast, lower Canny thresholds, or reduce blur sigma.
- **Too many tiny contours?** Increase area filter, erode/dilate, or increase thresholds.
- **Jagged boxes?** Use `cv2.GaussianBlur` before Canny; try `L2gradient=True`.
- **Lighting changes?** Prefer Canny or Otsu over a fixed threshold. Consider adaptive threshold:
  ```python
  adp = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, 11, 2)
  ```

---

## 8) Bonus: Morphology to clean edges
```python
kernel = np.ones((3,3), np.uint8)
clean = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)  # bridge gaps
```

---

## 9) Next steps
- Contour moments (`cv2.moments`) for centroid/orientation
- Rotated boxes: `cv2.minAreaRect` for angle & tight bounds
- Object tracking: edges/contours per frame in video
- Real projects: sheet counting, bottle inspection, packaging pick‑and‑place ROIs

**You’re set.** Swap in your image and tune thresholds. For a notebook version with inline displays, say the word and I’ll convert this to `.ipynb`.
