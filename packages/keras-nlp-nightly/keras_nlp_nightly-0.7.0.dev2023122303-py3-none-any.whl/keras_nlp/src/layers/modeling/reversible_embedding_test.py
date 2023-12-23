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

import os

import numpy as np
from absl.testing import parameterized

from keras_nlp.src.backend import config
from keras_nlp.src.backend import keras
from keras_nlp.src.backend import ops
from keras_nlp.src.backend import random
from keras_nlp.src.layers.modeling.reversible_embedding import ReversibleEmbedding
from keras_nlp.src.tests.test_case import TestCase


class ReversibleEmbeddingTest(TestCase):
    @parameterized.named_parameters(
        ("tie_weights", True),
        ("untie_weights", False),
    )
    def test_layer_behaviors_tied(self, tie_weights):
        self.run_layer_test(
            cls=ReversibleEmbedding,
            init_kwargs={
                "input_dim": 100,
                "output_dim": 32,
                "tie_weights": tie_weights,
                "embeddings_initializer": "HeNormal",
            },
            input_data=random.randint(minval=0, maxval=100, shape=(4, 10)),
            expected_output_shape=(4, 10, 32),
            expected_num_trainable_weights=1 if tie_weights else 2,
        )

    def test_correctness(self):
        layer = ReversibleEmbedding(input_dim=3, output_dim=2)
        layer.build()
        layer.embeddings.assign(np.array([[0.0, 0.0], [2.0, 2.0], [3.0, 3.0]]))
        out = layer(np.array(([2, 1, 0])))
        self.assertAllClose(out, np.array([[3.0, 3.0], [2.0, 2.0], [0.0, 0.0]]))

        layer = ReversibleEmbedding(input_dim=3, output_dim=2)
        layer.build()
        layer.embeddings.assign(np.array([[0.0, 0.0], [2.0, 2.0], [3.0, 3.0]]))
        out = layer(np.array(([[1.0, 1.0]])), reverse=True)
        self.assertAllClose(out, np.array([[0.0, 4.0, 6.0]]))

    def test_tied_checkpoint_untied_weights(self):
        embedding = ReversibleEmbedding(100, 16, tie_weights=True)
        inputs = keras.Input(shape=(10,), dtype="int32")
        hidden_states = embedding(inputs)
        outputs = embedding(hidden_states, reverse=True)
        tied_model = keras.Model(inputs, outputs)
        path = os.path.join(self.get_temp_dir(), "checkpoint.weights.h5")
        tied_model.save_weights(path)

        embedding = ReversibleEmbedding(100, 16, tie_weights=False)
        inputs = keras.Input(shape=(10,), dtype="int32")
        hidden_states = embedding(inputs)
        outputs = embedding(hidden_states, reverse=True)
        untied_model = keras.Model(inputs, outputs)
        untied_model.load_weights(path)

        input_data = ops.ones(shape=(4, 10), dtype="int32")
        self.assertAllClose(untied_model(input_data), tied_model(input_data))

    def test_reverse_dtype(self):
        embedding = ReversibleEmbedding(100, 16, reverse_dtype="float32")
        input_data = ops.ones(shape=(4, 10, 16))
        output_data = embedding(input_data, reverse=True)
        self.assertEqual(output_data.shape, (4, 10, 100))
        self.assertDTypeEqual(output_data, "float32")

        if config.backend() == "torch":
            import torch

            if not torch.cuda.is_available():
                self.skipTest("Torch CPU does not support float16")

        embedding = ReversibleEmbedding(100, 16, reverse_dtype="float16")
        input_data = ops.ones(shape=(4, 10, 16))
        output_data = embedding(input_data, reverse=True)
        self.assertEqual(output_data.shape, (4, 10, 100))
        self.assertDTypeEqual(output_data, "float16")

