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
from keras_nlp.src.api_export import keras_nlp_export
from keras_nlp.src.backend import keras
from keras_nlp.src.backend import ops
from keras_nlp.src.layers.modeling.reversible_embedding import ReversibleEmbedding
from keras_nlp.src.models.backbone import Backbone
from keras_nlp.src.models.llama.llama_decoder import LlamaDecoder
from keras_nlp.src.models.llama.llama_layernorm import LlamaLayerNorm


def _llama_kernel_initializer(stddev=0.02):
    return keras.initializers.RandomNormal(stddev=stddev)


@keras_nlp_export("keras_nlp.models.LlamaBackbone")
class LlamaBackbone(Backbone):
    """
    LLaMA core network with hyperparameters.

    This network implements a Transformer-based decoder network,
    LLaMA, as described in ["LLaMA: Open Foundation and Fine-Tuned Language Models"](https://arxiv.org/abs/2302.13971).

    The default constructor gives a fully customizable, randomly initialized
    LLaMA model with any number of layers, heads, and embedding
    dimensions. This backbone also supports LLaMA2 checkpoints.

    Args:
        vocabulary_size: int. The size of the token vocabulary.
        num_layers: int. The number of transformer layers.
        num_query_heads: int. The number of attention heads for each transformer.
            The hidden size must be divisible by the number of attention heads.
        hidden_dim: int. The size of the transformer encoding and pooler layers.
        intermediate_dim: int. The output dimension of the first Dense layer in
            a two-layer feedforward network for each transformer.
        num_key_value_heads: int. This is the number of key_value heads that
            should be used to implement Grouped Query Attention. If num_key_value_heads=num_attention_heads,
            the model will use Multi Head Attention (MHA), if num_key_value_heads=1
            the model will use Multi Query Attention (MQA)
        rope_scaling_factor: float. The scaling factor for calculation of rotary
            embedding
        rope_max_wavelength: int. The maximum angular wavelength of the
            sine/cosine curves, for rotary embeddings.
        layer_norm_epsilon: float. a value added to the denominator for
            numerical stability.
        max_sequence_length: int. The maximum sequence length that this encoder
            can consume. If `None`, `max_sequence_length` uses the value from
            sequence length. This determines the variable shape for positional
            embeddings.

    """

    def __init__(
        self,
        vocabulary_size,
        num_layers,
        num_query_heads,
        hidden_dim,
        intermediate_dim,
        num_key_value_heads,
        rope_scaling_factor=1.0,
        rope_max_wavelength=10000,
        layer_norm_epsilon=1e-5,
        max_sequence_length=4096,
        **kwargs,
    ):
        # Inputs
        token_ids = keras.Input(shape=(None,), dtype="int32", name="token_ids")
        padding_mask = keras.Input(
            shape=(None,), dtype="int32", name="padding_mask"
        )

        # Embed tokens
        token_embedding = ReversibleEmbedding(
            input_dim=vocabulary_size,
            output_dim=hidden_dim,
            embeddings_initializer=_llama_kernel_initializer(stddev=0.01),
            tie_weights=False,
            name="token_embedding",
        )(token_ids)

        x = token_embedding

        # Apply successive transformer decoder blocks.
        for i in range(num_layers):
            x = LlamaDecoder(
                intermediate_dim=intermediate_dim,
                num_query_heads=num_query_heads,
                num_key_value_heads=num_key_value_heads,
                rope_scaling_factor=rope_scaling_factor,
                max_sequence_length=max_sequence_length,
                rope_max_wavelength=rope_max_wavelength,
                layer_norm_epsilon=layer_norm_epsilon,
                activation=ops.silu,
                kernel_initializer=_llama_kernel_initializer(stddev=0.02),
                name=f"transformer_layer_{i}",
            )(x, decoder_padding_mask=padding_mask)

        sequence_output = LlamaLayerNorm(
            name="layer_norm",
            epsilon=layer_norm_epsilon,
        )(x)

        # Instantiate using Functional API Model constructor
        super().__init__(
            inputs={
                "token_ids": token_ids,
                "padding_mask": padding_mask,
            },
            outputs=sequence_output,
            **kwargs,
        )
        # All references to `self` below this line
        self.vocabulary_size = vocabulary_size
        self.num_layers = num_layers
        self.num_query_heads = num_query_heads
        self.hidden_dim = hidden_dim
        self.intermediate_dim = intermediate_dim
        self.rope_max_wavelength = rope_max_wavelength
        self.num_key_value_heads = num_key_value_heads
        self.rope_scaling_factor = rope_scaling_factor
        self.max_sequence_length = max_sequence_length
        self.layer_norm_epsilon = layer_norm_epsilon

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "vocabulary_size": self.vocabulary_size,
                "num_layers": self.num_layers,
                "num_query_heads": self.num_query_heads,
                "hidden_dim": self.hidden_dim,
                "intermediate_dim": self.intermediate_dim,
                "rope_max_wavelength": self.rope_max_wavelength,
                "rope_scaling_factor": self.rope_scaling_factor,
                "num_key_value_heads": self.num_key_value_heads,
                "max_sequence_length": self.max_sequence_length,
                "layer_norm_epsilon": self.layer_norm_epsilon,
            }
        )
        return config

    @property
    def token_embedding(self):
        return self.get_layer("token_embedding")

