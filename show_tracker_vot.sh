DEPLOY_PROTO='./nets/tracker.prototxt'
CAFFE_MODEL='./nets/tracker.caffemodel'
TEST_DATA_PATH='/home/ubuntu/GOTURN_py/data/images/'
OUTPUT_DIR='/home/ubuntu/GOTURN_py/data/output_images/'

python -m goturn.test.show_tracker_vot \
	--p $DEPLOY_PROTO \
	--m $CAFFE_MODEL \
	--i $TEST_DATA_PATH \
    --o $OUTPUT_DIR \
	--g 0
