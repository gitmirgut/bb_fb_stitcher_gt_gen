import matplotlib.pyplot as plt
import numpy as np

from composer import helpers
from gt_generator.draggable_marker import DraggableMarker, DraggableMarkerStack
from gt_generator.draggable_marker import dms_to_pts


class PointPicker(object):
    """GUI for picking points."""

    def __init__(self, img_l, right_img):
        self.img_l = img_l
        self.right_img = right_img
        self.count_dms_left = 0
        self.count_dms_right = 0

    def pick(self, selected = False):
        """Initialise GUI to pick 4 points on each side.

        A matplot GUI will be initialised, where the user has to pick 4 points
        on the left and right image. Afterwards the PointPicker will return 2
        clockwise sorted list of the picked points.
        """

        def _on_click(event):
            if event.button == 1 and event.dblclick:
                if event.inaxes == ax_left:
                    self.count_dms_left += 1
                    marker, = ax_left.plot(event.xdata, event.ydata, 'xr', markersize=10, markeredgewidth=2)
                    dm = DraggableMarker(marker, self.img_l, self.count_dms_left)
                    dm.connect()
                    dms_left.append(dm)
                elif event.inaxes == ax_right and len(dms_right) <= len(dms_left):
                    self.count_dms_right += 1
                    marker, = ax_right.plot(event.xdata, event.ydata, 'xr', markersize=10, markeredgewidth=2)
                    dm = DraggableMarker(marker, self.img_l, self.count_dms_right)
                    dm.connect()
                    dms_right.append(dm)

        fig, (ax_left, ax_right) = plt.subplots(
            nrows=1, ncols=2, tight_layout=False)
        plt.setp(ax_right.get_yticklabels(), visible=False)

        #  display images
        ax_left.imshow(self.img_l)
        ax_right.imshow(self.right_img)

        # Initialize list for storing the DraggableMarkers
        dms_left = DraggableMarkerStack()
        dms_right = DraggableMarkerStack()

        # TODO c_id
        c_id = fig.canvas.mpl_connect('button_press_event', _on_click)
        plt.show()
        # assert ((len(dms_left) == 4) and (len(dms_right) == 4))
        # points_left = dms_to_pts(dms_left)
        # points_right = dms_to_pts(dms_right)
        if selected is True:
            points_left = dms_left.get_selected_pts()
            points_right = dms_right.get_selected_pts()
        else:
            points_left = dms_left.get_pts()
            points_right = dms_right.get_pts()

        return points_left, points_right
