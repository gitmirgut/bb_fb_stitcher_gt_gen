import cv2
import numpy as np
import sys


def draw_makers(img, pts, color=(0, 0, 255),
                marker_types=cv2.MARKER_TILTED_CROSS):
    if pts is None:
        return img
    img_m = np.copy(img)
    pts = pts[0].astype(int)
    for i, pt in enumerate(pts):
        cv2.drawMarker(img_m, tuple(pt), color, markerType=marker_types,
                       markerSize=20, thickness=3)
        cv2.putText(img_m, str(i), tuple(pt), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255))
    return img_m

def draw_makers_with_id(img, pts, id, color=(0, 0, 255),
                marker_types=cv2.MARKER_TILTED_CROSS):
    if pts is None:
        return img
    img_m = np.copy(img)
    pts = pts[0].astype(int)
    for i, pt in enumerate(pts):
        cv2.drawMarker(img_m, tuple(pt), color, markerType=marker_types,
                       markerSize=40, thickness=10)
        cv2.putText(img_m, str(id) + '_' + str(i), tuple([pt[0]+15, pt[1]+15]), cv2.FONT_HERSHEY_SIMPLEX,0.5,color)
    return img_m

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    From: http://code.activestate.com/recipes/577058/
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")