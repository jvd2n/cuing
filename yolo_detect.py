from re import S
import tensorflow as tf
from tensorflow.python import saved_model
import core.utils as utils
from tensorflow.python.saved_model import tag_constants
import cv2
import numpy as np

MODEL_PATH = 'C:/Users/bit/yolov4/tensorflow-yolov4-tflite/checkpoints/yolov4-416'
IOU_THRESHOLD = 0.45
SCORE_THRESHOLD = 0.25
INPUT_SIZE = 416

# load model
saved_model_loaded = tf.saved_model.load(
    MODEL_PATH, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']


def main(img_path):     # 이미지 전처리
    img = cv2.imread(img_path)      # 이미지 읽어오기
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # 이미지 컬러 시스템 변경(BGR -> RGB)

    img_input = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))       # 이미지 크기 변경
    img_input = img_input / 255.
    img_input = img_input[np.newaxis, ...].astype(
        np.float32)   # newaxis : 차원 1개 추가
    img_input = tf.constant(img_input)      # numpy array를 tensor로 바꿔줌

    pred_bbox = infer(img_input)        # bounding box로 후처리

    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=IOU_THRESHOLD,
        score_threshold=SCORE_THRESHOLD)

    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(),
                 valid_detections.numpy()]
    result = utils.draw_bbox(img, pred_bbox)        # 결과값을 bounding box로 그림

    result = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)  # BGR에서 RGB로 변환
    cv2.imwrite('result.png', result)   # opencv로 저장하려면 윗줄 과정 필요


if __name__ == '__main__':
    img_path = 'C:/Users/bit/yolov4/tensorflow-yolov4-tflite/data/table.jpg'
    main(img_path)

