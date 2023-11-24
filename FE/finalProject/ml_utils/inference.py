"""Translate an image to another image
An example of command-line usage is:
python export_graph.py --model models/Hazy_to_Clear.pb \
                       --input_dir input \
                       --output_dir output \
                       --image_size 256
"""

import os
import tensorflow as tf
from absl import app, flags
from . import utils

FLAGS = flags.FLAGS

flags.DEFINE_string('model', 'ml_models/Hazy_to_Clear.pb', 'model path (.pb)')
flags.DEFINE_string('input_file', None, 'input file path')  # 파일 경로를 입력 받도록 변경
flags.DEFINE_string('output_file', None, 'output file path')  # 파일 경로를 출력 받도록 변경
flags.DEFINE_integer('image_size', 256, 'image size, default: 256')


def inference(input_file, output_file, model_path, image_size):
    graph = tf.Graph()
    with graph.as_default():
        with tf.io.gfile.GFile(input_file, 'rb') as f:
            image_data = f.read()
            input_image = tf.image.decode_jpeg(image_data, channels=3)
            input_image = tf.image.resize(input_image, size=(image_size, image_size))
            input_image = utils.convert2float(input_image)
            input_image.set_shape([image_size, image_size, 3])

            with tf.io.gfile.GFile(model_path, 'rb') as model_file:  # 여기를 수정함
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(model_file.read())
                [output_image] = tf.import_graph_def(graph_def,
                                                     input_map={'input_image': input_image},
                                                     return_elements=['output_image:0'],
                                                     name='output')
            with tf.compat.v1.Session(graph=graph):
                generated = output_image.eval()

            with open(output_file, 'wb') as f:
                f.write(generated)


def main(unused_argv):
    inference()


if __name__ == '__main__':
    app.run(main)
