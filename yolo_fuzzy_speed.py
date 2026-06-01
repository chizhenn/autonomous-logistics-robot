"""
yolo_fuzzy_speed.py
Standalone: webcam person detection (YOLOv11) + fuzzy logic speed control.
No hardware. Estimates person distance from bounding box, then displays
the required robot speed (m/s) on screen. Uses the NEAREST person.
 
Run:
    pip install -U ultralytics opencv-python scikit-fuzzy "numpy<2"
    python3 yolo_fuzzy_speed.py
Press q to quit.
"""
 
import cv2
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from ultralytics import YOLO
 
# ---- Distance estimation calibration ----
PX_HEIGHT_AT_1M = 600.0
MAX_DIST = 5.0  # metres, clamp
 
# ---- Fuzzy logic controller ----
distance = ctrl.Antecedent(np.arange(0, 5.01, 0.05), 'distance')
speed = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'speed')
 
distance['near']   = fuzz.trimf(distance.universe, [0, 0, 1.5])
distance['medium'] = fuzz.trimf(distance.universe, [1.0, 2.25, 3.5])
distance['far']    = fuzz.trimf(distance.universe, [3.0, 5.0, 5.0])
 
speed['slow']     = fuzz.trimf(speed.universe, [0, 0, 0.2])
speed['moderate'] = fuzz.trimf(speed.universe, [0.3, 0.5, 0.7])
speed['fast']     = fuzz.trimf(speed.universe, [0.8, 1.0, 1.0])
 
rules = [
    ctrl.Rule(distance['near'],   speed['slow']),
    ctrl.Rule(distance['medium'], speed['moderate']),
    ctrl.Rule(distance['far'],    speed['fast']),
]
sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
 
 
def required_speed(dist_m):
    sim.input['distance'] = float(np.clip(dist_m, 0, MAX_DIST))
    sim.compute()
    return sim.output['speed']
 
 
# ---- Detection loop ----
model = YOLO('yolo11n.pt')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam. Try VideoCapture(1) or 2.")
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
 
    results = model(frame, classes=[0], verbose=False)  # class 0 = person
    boxes = results[0].boxes
 
    nearest_dist = None  # smallest distance = closest person
    for b in boxes:
        x1, y1, x2, y2 = map(int, b.xyxy[0])
        box_h = y2 - y1
        if box_h <= 0:
            continue
        dist = PX_HEIGHT_AT_1M / box_h  # closer -> taller box -> smaller dist
        dist = min(dist, MAX_DIST)
        if nearest_dist is None or dist < nearest_dist:
            nearest_dist = dist
        conf = float(b.conf[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"person {conf:.2f}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
 
    # No person -> path clear -> full speed
    v = required_speed(nearest_dist) if nearest_dist is not None else 1.0
    label = f"Required speed: {v:.2f} m/s"
    if nearest_dist is not None:
        label += f"  (nearest {nearest_dist:.2f} m)"
    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
 
    cv2.imshow("YOLOv11 + Fuzzy Speed Control", frame)
    if cv2.waitKey(1) == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()