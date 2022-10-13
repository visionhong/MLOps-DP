import json
from typing import List

import tensorflow as tf
import tensorflow_hub as hub

def get_label(json_path: str = "./image_net_labels.json") -> List[str]:
    with open(json_path, 'r') as f:
        labels = json.load(f)
    return labels

def load_hub_model() -> tf.keras.Model:
    model = tf.keras.Sequential([hub.KerasLayer("https://tfhub.dev/google/imagenet/inception_v3/classification/4")])
    model.build([None, 299, 299, 3])
    return model

class InceptionV3Model(tf.keras.Model):
    def __init__(self, model: tf.keras.Model, labels: List[str]):
        super(InceptionV3Model, self).__init__()
        self.model = model
        self.labels = labels

    # @tf.function 데코레이션을 사용하면 tf 1.x 스타일로 해당 함수 내의 로직이 동작해서 상황에 따라 속도가 약간 빨라질 수 있음
    @tf.function(input_signature=[tf.TensorSpec(shape=[None], dtype=tf.string, name="image")])
    def serving_fn(self, input_img: str) -> tf.Tensor:
        def _base64_to_array(img):
            img = tf.io.decode_base64(img)
            img = tf.io.decode_jpeg(img)
            img = tf.image.convert_image_dtype(img, tf.float32)
            img = tf.image.resize(img, (299, 299))
            img = tf.reshape(img, (299, 299, 3))
            return img

        # inference
        img = tf.map_fn(_base64_to_array, input_img, dtype=tf.float32)
        predictions = self.model(img)

        def _convert_to_label(predictions):
            max_prob = tf.math.reduce_max(predictions)  # softmax 결과에서 가장 확률이 높은 클래스 선택
            idx = tf.where(tf.equal(predictions, max_prob))  # 클래스 인덱스 get
            label = tf.squeeze(tf.gather(self.labels, idx))  # 라벨 목록에서 라벨 get
            return label

        return tf.map_fn(_convert_to_label, predictions, dtype=tf.string)

    def save(self, export_path="./saved_model/inception_v3/"):
        signatures = {"serving_default": self.serving_fn}
        tf.keras.backend.set_learning_phase(0)  # torch의 model.eval()과 비슷 / 0: test 1: train
        tf.saved_model.save(self, export_path, signatures=signatures)

def main():
    labels = get_label(json_path="./image_net_labels.json")
    inception_v3_hub_model = load_hub_model()
    inception_v3_model = InceptionV3Model(inception_v3_hub_model, labels)
    version_number = 0
    inception_v3_model.save(export_path=f"./saved_model/inception_v3/{version_number}")

if __name__ == '__main__':
    main()
