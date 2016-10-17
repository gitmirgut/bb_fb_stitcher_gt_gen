import cv2
import numpy as np

def draw_makers(img, pts, color=(0, 0, 255),
                marker_types=cv2.MARKER_TILTED_CROSS):
    print(pts)
    if pts is None:
        return img
    img_m = np.copy(img)
    pts = pts[0].astype(int)
    for i, pt in enumerate(pts):
        cv2.drawMarker(img_m, tuple(pt), color, markerType=marker_types,
                       markerSize=40, thickness=3)
        cv2.putText(img_m, str(i), tuple(pt), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255))
    return img_m