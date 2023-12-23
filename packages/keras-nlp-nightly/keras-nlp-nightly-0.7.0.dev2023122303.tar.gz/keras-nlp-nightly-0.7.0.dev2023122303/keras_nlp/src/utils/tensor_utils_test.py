# Copyright 2023 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf

from keras_nlp.src.backend import ops
from keras_nlp.src.tests.test_case import TestCase
from keras_nlp.src.utils.tensor_utils import convert_to_ragged_batch
from keras_nlp.src.utils.tensor_utils import tensor_to_list


class TensorToListTest(TestCase):
    def test_ragged_input(self):
        input_data = tf.ragged.constant([[1, 2], [4, 5, 6]])
        list_output = tensor_to_list(input_data)
        self.assertAllEqual(list_output, [[1, 2], [4, 5, 6]])

    def test_dense_input(self):
        input_data = tf.constant([[1, 2], [3, 4]])
        list_output = tensor_to_list(input_data)
        self.assertAllEqual(list_output, [[1, 2], [3, 4]])

    def test_scalar_input(self):
        input_data = tf.constant(1)
        list_output = tensor_to_list(input_data)
        self.assertEqual(list_output, 1)

    def test_ragged_strings(self):
        input_data = tf.ragged.constant([["▀▁▂▃", "samurai"]])
        detokenize_output = tensor_to_list(input_data)
        self.assertAllEqual(detokenize_output, [["▀▁▂▃", "samurai"]])

    def test_dense_strings(self):
        input_data = tf.constant([["▀▁▂▃", "samurai"]])
        detokenize_output = tensor_to_list(input_data)
        self.assertAllEqual(detokenize_output, [["▀▁▂▃", "samurai"]])

    def test_scalar_string(self):
        input_data = tf.constant("▀▁▂▃")
        detokenize_output = tensor_to_list(input_data)
        self.assertEqual(detokenize_output, "▀▁▂▃")

    def test_string_with_utf8_error(self):
        input_data = tf.constant([b"hello\xf2\xf1\x91\xe5"])
        detokenize_output = tensor_to_list(input_data)
        self.assertEqual(detokenize_output, ["hello"])


class ConvertToRaggedBatch(TestCase):
    def test_convert_1d_python(self):
        inputs = [1, 2]
        outputs, unbatched, rectangular = convert_to_ragged_batch(inputs)
        self.assertIsInstance(outputs, tf.RaggedTensor)
        self.assertAllEqual(outputs, [[1, 2]])
        self.assertTrue(unbatched)
        self.assertTrue(rectangular)

    def test_convert_2d_python(self):
        inputs = [[1, 2], [2]]
        outputs, unbatched, rectangular = convert_to_ragged_batch(inputs)
        self.assertIsInstance(outputs, tf.RaggedTensor)
        self.assertAllEqual(outputs, [[1, 2], [2]])
        self.assertFalse(unbatched)
        self.assertFalse(rectangular)

    def test_convert_1d_tensor(self):
        inputs = ops.array([1, 2, 3])
        outputs, unbatched, rectangular = convert_to_ragged_batch(inputs)
        self.assertIsInstance(outputs, tf.RaggedTensor)
        self.assertAllEqual(outputs, [[1, 2, 3]])
        self.assertTrue(unbatched)
        self.assertTrue(rectangular)

    def test_convert_2d_tensor(self):
        inputs = ops.array([[1, 2, 3], [1, 2, 3]])
        outputs, unbatched, rectangular = convert_to_ragged_batch(inputs)
        self.assertIsInstance(outputs, tf.RaggedTensor)
        self.assertAllEqual(outputs, [[1, 2, 3], [1, 2, 3]])
        self.assertFalse(unbatched)
        self.assertTrue(rectangular)

    def test_convert_ragged(self):
        inputs = tf.ragged.constant([[1, 2], [1]])
        outputs, unbatched, rectangular = convert_to_ragged_batch(inputs)
        self.assertIsInstance(outputs, tf.RaggedTensor)
        self.assertAllEqual(outputs, [[1, 2], [1]])
        self.assertFalse(unbatched)
        self.assertFalse(rectangular)

