# Date: Friday 02 June 2017 05:04:00 PM IST 
# Email: nrupatunga@whodat.com
# Name: Nrupatunga
# Description: Basic regressor function implemented

from __future__ import print_function
import os


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
        self.bbox_gt = bbox_gt
        self.bbox_curr_prior_tight = bbox_gt
        objRegressor.init()