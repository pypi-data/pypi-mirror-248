from aicmder.torch import transformer
from aicmder.torch.transformer import Embeddings
try:
    from multi_headed_attn import MultiHeadedAttention
except:
    from aicmder.torch.transformer import MultiHeadedAttention
import torch.nn as nn
from aicmder.torch.transformer import LayerNorm, PositionwiseFeedForward, RMSNorm, MLP
from aicmder.torch.transformer.multi_headed_attn import ATTEN_TYPE_HYGRA, ATTEN_TYPE_SELF
import torch
from aicmder.torch.transformer.util_class import ActivationFunction, ModelOutput

# https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/encoders/encoder.py
"""Base class for encoders and generic multi encoders."""
import torch.nn as nn
# from aicmder.torch.transformer.misc import aeq

from aicmder.torch.transformer.base_model import EncoderBase
from dataclasses import dataclass
from typing import Optional, Tuple

class EncoderLayer(nn.Module):

    def __init__(self, heads, d_model, dropout, max_relative_pos, d_ff, use_neg_dist=True, pos_ffn_activation_fn=ActivationFunction.relu, rmsnorm=False):
        super(EncoderLayer, self).__init__()
        self.attention = MultiHeadedAttention(head_count=heads, model_dim=d_model,
                                              dropout=dropout,
                                              max_relative_positions=max_relative_pos,
                                              use_neg_dist=use_neg_dist)
        self.dropout = nn.Dropout(dropout)
        LayerNormFunc = RMSNorm if rmsnorm else LayerNorm
        layernorm_epsilon = 1e-6
        self.layer_norm = LayerNormFunc(d_model, eps=layernorm_epsilon)
        # self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)
        self.feed_forward = PositionwiseFeedForward(
            d_model, d_ff, dropout, activation_fn=pos_ffn_activation_fn)
        # self.feed_forward = MLP(d_model, d_ff / 2)
        self.post_attention_layernorm = LayerNormFunc(d_model, eps=layernorm_epsilon)

    def forward(self, inputs, mask, attn_type=ATTEN_TYPE_SELF):
        # post-norm original
        # context, attn_per_head = self.attention(
        #     inputs, inputs, inputs, mask=mask, attn_type=attn_type)
        # out = self.layer_norm(self.dropout(context) + inputs)
        # return self.feed_forward(out), attn_per_head
        
        # pre-norm
        input_norm = self.layer_norm(inputs)
        # input_norm = inputs
        context, attn_per_head = self.attention(input_norm, input_norm, input_norm,
                                    mask=mask, attn_type=attn_type)
        out = self.dropout(context) + inputs
        return self.feed_forward(out), attn_per_head
        ############################# origin above
        # layernorm_output = self.post_attention_layernorm(out)
        # output = self.feed_forward(layernorm_output) # residual
        # return output, attn_per_head


    def update_dropout(self, dropout, attention_dropout):
        self.attention.update_dropout(attention_dropout)
        self.feed_forward.update_dropout(dropout)
        self.dropout.p = dropout

# https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/encoders/transformer.py
class TransformerEncoder(EncoderBase):
    """The Transformer encoder from "Attention is All You Need"
    :cite:`DBLP:journals/corr/VaswaniSPUJGKP17`

    ```mermaid

       graph BT
          A[input]
          B[multi-head self-attn]
          C[feed forward]
          O[output]
          A --> B
          B --> C
          C --> O
    ```
    Args:
        num_layers (int): number of encoder layers
        d_model (int): size of the model
        heads (int): number of heads
        d_ff (int): size of the inner FF layer
        dropout (float): dropout parameters
        embeddings (onmt.modules.Embeddings):
          embeddings to use, should have positional encodings
        pos_ffn_activation_fn (ActivationFunction):
            activation function choice for PositionwiseFeedForward layer

    Returns:
        (torch.FloatTensor, torch.FloatTensor):

        * embeddings ``(src_len, batch_size, model_dim)``
        * memory_bank ``(src_len, batch_size, model_dim)``
    """
    def __init__(self, heads, d_model, dropout, max_relative_positions, d_ff,
                 use_neg_dist=True, num_layers=6, attn_type=ATTEN_TYPE_SELF,
                 pos_ffn_activation_fn=ActivationFunction.relu, embeddings=None, check_device=False):

        super(TransformerEncoder, self).__init__()

        self.num_layers = num_layers
        if isinstance(max_relative_positions, int):
            max_relative_positions = [max_relative_positions] * self.num_layers
        assert len(max_relative_positions) == self.num_layers

        self.attn_types = [attn_type] * self.num_layers
        assert len(self.attn_types) == self.num_layers

        self.layer = nn.ModuleList(
            [EncoderLayer(heads,
                          d_model,
                          dropout,
                          max_relative_pos=max_relative_positions[i],
                          d_ff=d_ff,
                          use_neg_dist=use_neg_dist,
                          pos_ffn_activation_fn=pos_ffn_activation_fn)
             for i in range(num_layers)])
        self.embeddings = embeddings
        self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)
        self.check_device = check_device


    def update_dropout(self, dropout, attention_dropout):
        if self.embeddings is not None:
            self.embeddings.update_dropout(dropout)
        for layer in self.layer:
            layer.update_dropout(dropout, attention_dropout)


    def forward(self, src, mask=None, lengths=None, token_type_ids=None, output_attentions=False):
        """
        Args:
            src (`FloatTensor`): `[batch_size x src_len x model_dim]`
            lengths (`LongTensor`): length of each sequence `[batch]`
        Returns:
            (`FloatTensor`):
            * outputs `[batch_size x src_len x model_dim]`
        """
        self._check_args(src, lengths)
        all_self_attentions = () if output_attentions else None

        if self.embeddings is not None:

            if token_type_ids is None:
                token_type_ids = torch.ones(src.shape, dtype=torch.long)
            if src.dim() == 2:
                src = src.unsqueeze(2)
            out = self.embeddings(src, step=0, token_type_ids=token_type_ids)


            # emb = self.embeddings(src)
            # out = emb.transpose(0, 1).contiguous()
        else:
            out = src

        if mask is None:
            mask = None if lengths is None else \
                ~sequence_mask(lengths, out.shape[1]).unsqueeze(1)
        # Run the forward pass of every layer of the tranformer.
        # representations = []
        # attention_scores = []
        for i in range(self.num_layers):
            current_layer = self.layer[i]

            if self.check_device:
                current_layer_device = next(current_layer.parameters()).device
                if out.device != current_layer_device:
                    out = out.to(current_layer_device)
                # if mask.device != current_layer_device:
                #     mask = mask.to(current_layer_device)

            # print(i, current_layer)
            out, attn_per_head = current_layer(
                out, mask, attn_type=self.attn_types[i])
            # representations.append(out)
            if output_attentions and attn_per_head is not None:
                # attention_scores.append(attn_per_head)
                all_self_attentions = all_self_attentions + (attn_per_head, )

        ## add layer norm
        representations = self.layer_norm(out)
        # return representations  # , attention_scores
        return EncoderOuput(
            last_hidden_state=representations,
            attentions=all_self_attentions,
        )

# modeling_roberta
@dataclass
class EncoderOuput(ModelOutput):
    last_hidden_state: torch.FloatTensor = None
    # past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None
    # hidden_states: Optional[Tuple[torch.FloatTensor]] = None
    attentions: Optional[Tuple[torch.FloatTensor]] = None
    # cross_attentions: Optional[Tuple[torch.FloatTensor]] = None


if __name__ == "__main__":
    from aicmder.torch import init_seeds
    from aicmder.torch.transformer import sequence_mask
    import torch
    init_seeds(0)
    heads = 8
    d_model = 512
    dropout = 0.2
    max_relative_positions = 32
    use_neg_dist = True
    d_ff = 2048
    # encoder = EncoderLayer(heads, d_model, dropout,
    #                        max_relative_positions, d_ff)

    # inputs = torch.rand(32, 5, d_model, dtype=torch.float32)
    # code_len = torch.zeros(32, dtype=torch.long)
    # code_len[:] = 5
    # print(inputs.shape)
    # mask = None if code_len is None else \
    #     ~sequence_mask(code_len, inputs.shape[1]).unsqueeze(1)
    # # context, attn_per_head = attention(inputs, inputs, inputs, mask=mask, attn_type=ATTEN_TYPE_SELF)
    # # context = encoder(inputs, mask=mask, attn_type=ATTEN_TYPE_HYGRA)
    # context = encoder(inputs, mask=mask, attn_type=ATTEN_TYPE_SELF)
    # print(context[0].shape, context[1].shape)
    # out = context[0]
    # print(out.shape, out.transpose(0, 1).contiguous().shape)


    word_embeddings = Embeddings(d_model, 184866, 0, position_encoding="default")
    src_input = torch.randint(0, 2000, (16, 7))


    transformer_encoder = TransformerEncoder(
        heads, d_model, dropout, max_relative_positions, d_ff, embeddings=word_embeddings)
    out = transformer_encoder(src_input, output_attentions=True)
    print(out[0].shape, out[1].shape)
