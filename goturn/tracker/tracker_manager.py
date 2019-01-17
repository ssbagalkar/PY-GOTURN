#te: Wednesday 07 June 2017 11:28:11 AM IST
# Email: nrupatunga@whodat.com
# Name: Nrupatunga
# Description: tracker manager

import cv2
import os
import sys

opencv_version = cv2.__version__.split('.')[0]

class tracker_manager:

    """Docstring for tracker_manager. """

    def __init__(self, videos, regressor, tracker, logger, out_path):
        """This is

        :videos: list of video frames and annotations
        :regressor: regressor object
        :tracker: tracker object
        :logger: logger object
        :data_path:output path
        :returns: list of video sub directories
        """

        self.videos = videos
        self.regressor = regressor
        self.tracker = tracker
        self.logger = logger
        self.out_path = out_path

        #Create output dir if not already present
        if not os.path.isdir(out_path):
            print("Output directory not present. Creating it at {}..".format(out_path))
            os.mkdir(out_path)
        else:
            print("Output directory already present")


    def trackAll(self, start_video_num, pause_val):
        """Track the objects in the video
        """

        videos = self.videos
        objRegressor = self.regressor
        objTracker = self.tracker
        logger = self.logger
        out_path = self.out_path

        video_keys = list(videos.keys())
        num_dirs_processed=0
        for i in range(start_video_num, len(videos)):
            print("Processing for {}".format(video_keys[i]))
            if not os.path.isdir(os.path.join(out_path, video_keys[i])):
                print("Creating directory for {} in path {}...".format(video_keys[i],out_path))
                os.mkdir(os.path.join(out_path,video_keys[i]))
            else:
                if len(os.listdir(os.path.join(out_path, video_keys[i])) ) != 0:
                    print("Directory already present and has images.Skipping...")
                    continue
                else:
                    print("Directory is present, but is empty.Writing images to it..")
            num_dirs_processed+=1
            current_case = video_keys[i]
            dir_to_write = os.path.join(out_path, video_keys[i])
            print("Created directory {}..".format(dir_to_write))
            video_frames = videos[video_keys[i]][0]
            annot_frames = videos[video_keys[i]][1]

            num_frames = min(len(video_frames), len(annot_frames))

            # Get the first frame of this video with the intial ground-truth bounding box
            frame_1 = video_frames[0]
            print("First frame is {}".format(frame_1))
            bbox_1 = annot_frames[0]
            print("First bbox is {}".format((int(bbox_1.x1), int(bbox_1.y1), int(bbox_1.x2), int(bbox_1.y2))))
            sMatImage = cv2.imread(frame_1)
            objTracker.init(sMatImage, bbox_1, objRegressor)
            print("Looping through the frames..")
            for i in range(1, num_frames):
                frame = video_frames[i]
                sMatImage = cv2.imread(frame)
                sMatImageDraw = sMatImage.copy()
                bbox = annot_frames[i]
                print("BBOX[GT]: {}".format((int(bbox.x1), int(bbox.y1), int(bbox.x2), int(bbox.y2))))

                if opencv_version == '2':
                    cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 255, 255), 2)
                else:
                    sMatImageDraw = cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 255, 255), 2)

                print("[INFO]:Tracking begins on frame {}".format(i))
                bbox_track = objTracker.track(sMatImage, objRegressor)
                if abs(int(bbox.x1)-int(bbox_track.x1)) > 10 or abs(int(bbox.x2)-int(bbox_track.x2)) > 10 or abs(int(bbox.y1)-int(bbox_track.y1)) > 10 or abs(int(bbox.y2)-int(bbox_track.y2)):
                    sys.exit()
                if bbox_track is not None:
                    print("BBOX[Predicted]: {}".format((int(bbox_track.x1), int(bbox_track.y1), int(bbox_track.x2), int(bbox_track.y2))))
                if opencv_version == '2':
                    cv2.rectangle(sMatImageDraw, (int(bbox_track.x1), int(bbox_track.y1)), (int(bbox_track.x2), int(bbox_track.y2)), (255, 0, 0), 2)
                else:
                    sMatImageDraw = cv2.rectangle(sMatImageDraw, (int(bbox_track.x1), int(bbox_track.y1)), (int(bbox_track.x2), int(bbox_track.y2)), (255, 0, 0))
                cv2.imwrite(os.path.join(dir_to_write,"img_0000"+str(i)+".png"),sMatImageDraw)
                print("Written {} to folder  {}".format("img_"+str(i), current_case))
            print("\n\n")
            print("-------------------------------------")
        print("Total number of folders processed : {} ".format(num_dirs_processed))

