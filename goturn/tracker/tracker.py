# Date: Friday 02 June 2017 05:04:00 PM IST
# Email: nrupatunga@whodat.com
# Name: Nrupatunga
# Description: Basic regressor function implemented

from __future__ import print_function
from ..helper.image_proc import cropPadImage
from ..helper.BoundingBox import BoundingBox


class tracker:
    """tracker class"""

    def __init__(self, show_intermediate_output, logger):
        """TODO: to be defined. """
        self.show_intermediate_output = show_intermediate_output
        self.logger = logger

    def init(self, image_curr, bbox_gt, objRegressor):
        """ initializing the first frame in the video
        """
        self.image_prev = image_curr
        self.bbox_prev_tight = bbox_gt
        self.bbox_curr_prior_tight = bbox_gt
        print("[INFO]:Initialized with {} {} {} {}".format( int(bbox_gt.x1), int(bbox_gt.y1), int(bbox_gt.x2), int(bbox_gt.y2) ))
        # objRegressor.init()

    def track(self, image_curr, objRegressor):
        """TODO: Docstring for tracker.
        :returns: TODO
        """
        print("Entered tracking function..")
        print("[INFO]:Passing {} {} {} {} to cropPadImage function..".format( int(bbox_gt.x1), int(bbox_gt.y1), int(bbox_gt.x2), int(bbox_gt.y2) ))
        target_pad, _, _,  _ = cropPadImage(self.bbox_prev_tight, self.image_prev)
        cur_search_region, search_location, edge_spacing_x, edge_spacing_y = cropPadImage(self.bbox_curr_prior_tight, image_curr)

        bbox_estimate = objRegressor.regress(cur_search_region, target_pad)
        print("[INFO]:BBox Estimate before correction {} {} {} {}".format( int(bbox_estimate[0,0]), int(bbox_estimate[0,1]), int(bbox_estimate[0,2]), int(bbox_estimate[0,3]) ))

        bbox_estimate = BoundingBox(bbox_estimate[0, 0], bbox_estimate[0, 1], bbox_estimate[0, 2], bbox_estimate[0, 3])

        # Inplace correction of bounding box
        #print("[INFO]:BBox Estimate before correction {} {} {} {}".format( int(bbox_gt.x1), int(bbox_gt.y1), int(bbox_gt.x2), int(bbox_gt.y2)  ))
        bbox_estimate.unscale(cur_search_region)
        bbox_estimate.uncenter(image_curr, search_location, edge_spacing_x, edge_spacing_y)

        self.image_prev = image_curr
        self.bbox_prev_tight = bbox_estimate
        self.bbox_curr_prior_tight = bbox_estimate

        return bbox_estimate
