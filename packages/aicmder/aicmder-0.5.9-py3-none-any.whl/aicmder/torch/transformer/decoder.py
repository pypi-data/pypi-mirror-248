# https://github.dev/OpenNMT/OpenNMT-py/blob/173e113b1220b32c1d03a0f8d3f9d44759c071de/onmt/decoders/transformer.py#L12
import torch
import torch.nn as nn
from aicmder.torch.transformer.util_class import ActivationFunction
from aicmder.torch.transformer import AverageAttention, \
PositionwiseFeedForward, sequence_mask
try:
    from multi_headed_attn import MultiHeadedAttention
except:
    from aicmder.torch.transformer import MultiHeadedAttention
from aicmder.torch.transformer.embedding import PADDING_INDEX
from aicmder.torch.transformer.multi_headed_attn import ATTEN_TYPE_SELF, ATTEN_TYPE_HYGRA
from aicmder.torch.transformer.base_model import DecoderBase

class DecoderLayerBase(nn.Module):

    def __init__(self,
                 d_model,
                 heads,
                 d_ff,
                 dropout,
                 attention_dropout,
                 self_attn_type="scaled-dot",
                 max_relative_positions=0,
                 aan_useffn=False,
                 full_context_alignment=False,
                 alignment_heads=0,
                 pos_ffn_activation_fn=ActivationFunction.relu):
        """
        Args:
            d_model (int): the dimension of keys/values/queries in
                :class:`MultiHeadedAttention`, also the input size of
                the first-layer of the :class:`PositionwiseFeedForward`.
            heads (int): the number of heads for MultiHeadedAttention.
            d_ff (int): the second-layer of the
                :class:`PositionwiseFeedForward`.
            dropout (float): dropout in residual, self-attn(dot) and
                feed-forward
            attention_dropout (float): dropout in context_attn  (and
                self-attn(avg))
            self_attn_type (string): type of self-attention scaled-dot,
                average
            max_relative_positions (int):
                Max distance between inputs in relative positions
                representations
            aan_useffn (bool): Turn on the FFN layer in the AAN decoder
            full_context_alignment (bool):
                whether enable an extra full context decoder forward for
                alignment
            alignment_heads (int):
                N. of cross attention heads to use for alignment guiding
            pos_ffn_activation_fn (ActivationFunction):
                activation function choice for PositionwiseFeedForward layer

        """
        super(DecoderLayerBase, self).__init__()

        if self_attn_type == "scaled-dot":
            self.self_attn = MultiHeadedAttention(
                head_count=heads,
                model_dim=d_model,
                dropout=attention_dropout,
                max_relative_positions=max_relative_positions,
            )
        elif self_attn_type == "average":
            self.self_attn = AverageAttention(
                d_model, dropout=attention_dropout, aan_useffn=aan_useffn
            )

        self.feed_forward = PositionwiseFeedForward(d_model, d_ff, dropout,
                                                    pos_ffn_activation_fn
                                                    )

        self.layer_norm_1 = nn.LayerNorm(d_model, eps=1e-6)
        # self.layer_norm = LayerNorm(d_model)

        self.drop = nn.Dropout(dropout)
        self.full_context_alignment = full_context_alignment
        self.alignment_heads = alignment_heads

    def forward(self, *args, **kwargs):
        """Extend `_forward` for (possibly) multiple decoder pass:
        Always a default (future masked) decoder forward pass,
        Possibly a second future aware decoder pass for joint learn
        full context alignement, :cite:`garg2019jointly`.

        Args:
            * All arguments of _forward.
            with_align (bool): whether return alignment attention.

        Returns:
            (FloatTensor, FloatTensor, FloatTensor or None):

            * output ``(batch_size, T, model_dim)``
            * top_attn ``(batch_size, T, src_len)``
            * attn_align ``(batch_size, T, src_len)`` or None
        """
        with_align = kwargs.pop("with_align", False)
        output, attns = self._forward(*args, **kwargs)
        if attns is not None:
            top_attn = attns[:, 0, :, :].contiguous()
        else:
            top_attn = attns
        attn_align = None
        if with_align:
            if self.full_context_alignment:
                # return _, (B, Q_len, K_len)
                _, attns = self._forward(*args, **kwargs, future=True)

            if self.alignment_heads > 0:
                attns = attns[:, : self.alignment_heads, :, :].contiguous()
            # layer average attention across heads, get ``(B, Q, K)``
            # Case 1: no full_context, no align heads -> layer avg baseline
            # Case 2: no full_context, 1 align heads -> guided align
            # Case 3: full_context, 1 align heads -> full cte guided align
            attn_align = attns.mean(dim=1)
        return output, top_attn, attn_align

    def update_dropout(self, dropout, attention_dropout):
        self.self_attn.update_dropout(attention_dropout)
        self.feed_forward.update_dropout(dropout)
        self.drop.p = dropout

    def _forward(self, *args, **kwargs):
        raise NotImplementedError

    def _compute_dec_mask(self, tgt_pad_mask, future):
        tgt_len = tgt_pad_mask.size(-1)
        if not future:  # apply future_mask, result mask in (B, T, T)
            future_mask = torch.ones(
                [tgt_len, tgt_len],
                device=tgt_pad_mask.device,
                dtype=torch.uint8,
            )
            future_mask = future_mask.triu_(1).view(1, tgt_len, tgt_len)
            # BoolTensor was introduced in pytorch 1.2
            try:
                future_mask = future_mask.bool()
            except AttributeError:
                pass
            dec_mask = torch.gt(tgt_pad_mask + future_mask, 0)
        else:  # only mask padding, result mask in (B, 1, T)
            dec_mask = tgt_pad_mask
        return dec_mask

    def _forward_self_attn(self, inputs_norm, dec_mask, layer_cache, step, attn_type=ATTEN_TYPE_SELF):
        if isinstance(self.self_attn, MultiHeadedAttention):
            return self.self_attn(
                inputs_norm,
                inputs_norm,
                inputs_norm,
                mask=dec_mask,
                layer_cache=layer_cache,
                attn_type=attn_type,
            )
        elif isinstance(self.self_attn, AverageAttention):
            return self.self_attn(
                inputs_norm, mask=dec_mask, layer_cache=layer_cache, step=step
            )
        else:
            raise ValueError(
                f"self attention {type(self.self_attn)} not supported"
            )



class DecoderLayer(DecoderLayerBase):
    """Transformer Decoder layer block in Pre-Norm style.
    Pre-Norm style is an improvement w.r.t. Original paper's Post-Norm style,
    providing better converge speed and performance. This is also the actual
    implementation in tensor2tensor and also avalable in fairseq.
    See https://tunz.kr/post/4 and :cite:`DeeperTransformer`.

    ```mermaid
        graph LR
        %% "*SubLayer" can be self-attn, src-attn or feed forward block
            A(input) --> B[Norm]
            B --> C["*SubLayer"]
            C --> D[Drop]
            D --> E((+))
            A --> E
            E --> F(out)
    ```
    
    """
    
    def __init__(
        self,
        d_model,
        heads,
        d_ff,
        dropout,
        attention_dropout,
        self_attn_type="scaled-dot",
        max_relative_positions=0,
        aan_useffn=False,
        full_context_alignment=False,
        alignment_heads=0,
        pos_ffn_activation_fn=ActivationFunction.relu,
    ):
        """
        Args:
            See TransformerDecoderLayerBase
        """
        super(DecoderLayer, self).__init__(
            d_model,
            heads,
            d_ff,
            dropout,
            attention_dropout,
            self_attn_type,
            max_relative_positions,
            aan_useffn,
            full_context_alignment,
            alignment_heads,
            pos_ffn_activation_fn=pos_ffn_activation_fn,
        )
        self.context_attn = MultiHeadedAttention(
            head_count=heads, model_dim=d_model, dropout=attention_dropout,
            max_relative_positions=max_relative_positions
        )
        self.layer_norm_2 = nn.LayerNorm(d_model, eps=1e-6)

    def update_dropout(self, dropout, attention_dropout):
        super(DecoderLayer, self).update_dropout(
            dropout, attention_dropout
        )
        self.context_attn.update_dropout(attention_dropout)
        

    def _forward(
        self,
        inputs,
        memory_bank,
        src_pad_mask,
        tgt_pad_mask,
        attn_type,
        layer_cache=None,
        step=None,
        future=False,
    ):
        """A naive forward pass for transformer decoder.

        # T: could be 1 in the case of stepwise decoding or tgt_len

        Args:
            inputs (FloatTensor): ``(batch_size, T, model_dim)``
            memory_bank (FloatTensor): ``(batch_size, src_len, model_dim)``
            src_pad_mask (bool): ``(batch_size, 1, src_len)``
            tgt_pad_mask (bool): ``(batch_size, 1, T)``
            layer_cache (dict or None): cached layer info when stepwise decode
            step (int or None): stepwise decoding counter
            future (bool): If set True, do not apply future_mask.

        Returns:
            (FloatTensor, FloatTensor):

            * output ``(batch_size, T, model_dim)``
            * attns ``(batch_size, head, T, src_len)``

        """
        dec_mask = None

        if inputs.size(1) > 1:
            # masking is necessary when sequence length is greater than one
            dec_mask = self._compute_dec_mask(tgt_pad_mask, future)

        # apply layer norm first
        inputs_norm = self.layer_norm_1(inputs)

        query, _ = self._forward_self_attn(
            inputs_norm, dec_mask, layer_cache, step, attn_type=attn_type
        )

        query = self.drop(query) + inputs

        query_norm = self.layer_norm_2(query)
        mid, attns = self.context_attn(
            memory_bank,
            memory_bank,
            query_norm,
            mask=src_pad_mask,
            layer_cache=layer_cache,
            attn_type=attn_type,
        )
        output = self.feed_forward(self.drop(mid) + query)

        return output, attns
    
    

class TransformerDecoderBase(DecoderBase):
    def __init__(self, d_model, copy_attn, embeddings, alignment_layer):
        super(TransformerDecoderBase, self).__init__()

        self.embeddings = embeddings

        # Decoder State
        self.state = {}

        # previously, there was a GlobalAttention module here for copy
        # attention. But it was never actually used -- the "copy" attention
        # just reuses the context attention.
        self._copy = copy_attn
        self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)

        self.alignment_layer = alignment_layer

    @classmethod
    def from_opt(cls, opt, embeddings):
        """Alternate constructor."""
        return cls(
            opt.dec_layers,
            opt.dec_rnn_size,
            opt.heads,
            opt.transformer_ff,
            opt.copy_attn,
            opt.self_attn_type,
            opt.dropout[0] if type(opt.dropout) is list else opt.dropout,
            opt.attention_dropout[0]
            if type(opt.attention_dropout) is list
            else opt.attention_dropout,
            embeddings,
            opt.max_relative_positions,
            opt.aan_useffn,
            opt.full_context_alignment,
            opt.alignment_layer,
            alignment_heads=opt.alignment_heads,
            pos_ffn_activation_fn=opt.pos_ffn_activation_fn,
        )

    def init_state(self, src_len, max_len):
        """Initialize decoder state."""
        self.state["src_len"] = src_len # [B]
        self.state["src_max_len"] = max_len  # an integer
        self.state["cache"] = None

    def map_state(self, fn):
        def _recursive_map(struct, batch_dim=0):
            for k, v in struct.items():
                if v is not None:
                    if isinstance(v, dict):
                        _recursive_map(v)
                    else:
                        struct[k] = fn(v, batch_dim)

        if self.state["src"] is not None:
            self.state["src"] = fn(self.state["src"], 1)
        if self.state["cache"] is not None:
            _recursive_map(self.state["cache"])


    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def update_dropout(self, dropout, attention_dropout):
        self.embeddings.update_dropout(dropout)
        for layer in self.transformer_layers:
            layer.update_dropout(dropout, attention_dropout)
            


class TransformerDecoder(TransformerDecoderBase):
    """The Transformer decoder from "Attention is All You Need".
    :cite:`DBLP:journals/corr/VaswaniSPUJGKP17`

    .. mermaid::

       graph BT
          A[input]
          B[multi-head self-attn]
          BB[multi-head src-attn]
          C[feed forward]
          O[output]
          A --> B
          B --> BB
          BB --> C
          C --> O


    Args:
        num_layers (int): number of decoder layers.
        d_model (int): size of the model
        heads (int): number of heads
        d_ff (int): size of the inner FF layer
        copy_attn (bool): if using a separate copy attention
        self_attn_type (str): type of self-attention scaled-dot, average
        dropout (float): dropout in residual, self-attn(dot) and feed-forward
        attention_dropout (float): dropout in context_attn (and self-attn(avg))
        embeddings (onmt.modules.Embeddings):
            embeddings to use, should have positional encodings
        max_relative_positions (int):
            Max distance between inputs in relative positions representations
        aan_useffn (bool): Turn on the FFN layer in the AAN decoder
        full_context_alignment (bool):
            whether enable an extra full context decoder forward for alignment
        alignment_layer (int): N° Layer to supervise with for alignment guiding
        alignment_heads (int):
            N. of cross attention heads to use for alignment guiding
    """

    def __init__(
        self,
        num_layers,
        d_model,
        heads,
        d_ff,
        embeddings=None,
        max_relative_positions=0,
        copy_attn=False,
        dropout=0.2,
        attention_dropout=0.2,
        aan_useffn=False,
        alignment_layer=None,
        full_context_alignment=False,
        alignment_heads=0,
        self_attn_type="scaled-dot",
        pos_ffn_activation_fn=ActivationFunction.relu,
    ):
        super(TransformerDecoder, self).__init__(
            d_model, copy_attn, embeddings, alignment_layer
        )

        self.transformer_layers = nn.ModuleList(
            [
                DecoderLayer(
                    d_model,
                    heads,
                    d_ff,
                    dropout,
                    attention_dropout,
                    self_attn_type=self_attn_type,
                    max_relative_positions=max_relative_positions,
                    aan_useffn=aan_useffn,
                    full_context_alignment=full_context_alignment,
                    alignment_heads=alignment_heads,
                    pos_ffn_activation_fn=pos_ffn_activation_fn,
                )
                for i in range(num_layers)
            ]
        )


    def forward(self, tgt, tgt_token_type_ids=None, memory_bank=None, src_pad_mask=None,  tgt_pad_mask=None, step=None, attn_type=ATTEN_TYPE_SELF, **kwargs):
        """Decode, possibly stepwise."""
        if memory_bank is None:
            memory_bank = self.embeddings(tgt)
        if step == 0:
            self._init_cache(memory_bank)

        # tgt_words = tgt[:, :, 0].transpose(0, 1)
        # tgt_words = tgt[:, :, 0]

        if self.embeddings is not None:
            if tgt_token_type_ids is None:
                tgt_token_type_ids = torch.ones(tgt.shape, dtype=torch.long)
            if tgt.dim() == 2:
                tgt = tgt.unsqueeze(2)
            emb = self.embeddings(tgt, step=0, token_type_ids=tgt_token_type_ids)

            # emb = self.embeddings(tgt, step=step)
            pad_idx = self.embeddings.word_padding_idx if self.embeddings is not None else PADDING_INDEX
            tgt_pad_mask = tgt.data.eq(pad_idx)
        else:
            emb = tgt
            assert tgt_pad_mask is not None, "target padding should be given."
        assert emb.dim() == 3  # len x batch x embedding_dim

        output = emb
        # output = emb.transpose(0, 1).contiguous()
        # src_memory_bank = memory_bank.transpose(0, 1).contiguous()


        # src_lens = kwargs["memory_lengths"]
        # src_max_len = self.state["src"].shape[0]

        if src_pad_mask is None:
            src_lens = self.state["src_len"]
            src_max_len = self.state["src_max_len"] 
            src_pad_mask = ~sequence_mask(src_lens, src_max_len).unsqueeze(1)
        
        if len(tgt_pad_mask.shape) == 2:
            tgt_pad_mask = tgt_pad_mask.unsqueeze(1)  # [B, 1, T_tgt]
            
        with_align = kwargs.pop("with_align", False)
        attn_aligns = []

        for i, layer in enumerate(self.transformer_layers):
            layer_cache = (
                self.state["cache"]["layer_{}".format(i)]
                if step is not None
                else None
            )
            src_memory_bank = memory_bank[i] if isinstance(memory_bank, list) else memory_bank
            output, attn, attn_align = layer(
                output,
                src_memory_bank,
                src_pad_mask,
                tgt_pad_mask,
                layer_cache=layer_cache,
                step=step,
                with_align=with_align,
                attn_type=attn_type
            )
            if attn_align is not None:
                attn_aligns.append(attn_align)

        output = self.layer_norm(output)
        # dec_outs = output.transpose(0, 1).contiguous()
        # attn = attn.transpose(0, 1).contiguous()
        dec_outs = output.contiguous()
        if attn is not None:
            attn = attn.contiguous()

        attns = {"std": attn}
        if self._copy:
            attns["copy"] = attn
        if with_align and self.alignment_layer is not None:
            attns["align"] = attn_aligns[self.alignment_layer]  # `(B, Q, K)`
            # attns["align"] = torch.stack(attn_aligns, 0).mean(0)  # All avg

        # TODO change the way attns is returned dict => list or tuple (onnx)
        return dec_outs, attns

    def _init_cache(self, memory_bank):
        self.state["cache"] = {}
        batch_size = memory_bank.size(1)
        depth = memory_bank.size(-1)

        for i, layer in enumerate(self.transformer_layers):
            layer_cache = {"memory_keys": None, "memory_values": None}
            if isinstance(layer.self_attn, AverageAttention):
                layer_cache["prev_g"] = torch.zeros(
                    (batch_size, 1, depth), device=memory_bank.device
                )
            else:
                layer_cache["self_keys"] = None
                layer_cache["self_values"] = None
            self.state["cache"]["layer_{}".format(i)] = layer_cache


if __name__ == "__main__":
    from aicmder.torch import init_seeds
    from aicmder.torch.transformer import sequence_mask, Embeddings
    import torch
    init_seeds(0)
    nlayers = 6
    input_size = 512
    trans_drop = 0.2
    num_head = 8
    d_ff = 2048
    coverage_attn = False

    tgt_word_embeddings = Embeddings(input_size, 184866, 0, position_encoding="default")
    decoder = TransformerDecoder(
                num_layers=nlayers,
                d_model=input_size,
                heads=num_head,
                d_ff=d_ff,
                copy_attn=False,
                embeddings=tgt_word_embeddings,
                # coverage_attn=coverage_attn,
                dropout=trans_drop
            ) 

    memory_bank = torch.rand(32, 5, input_size, dtype=torch.float32)
    # tgt = torch.rand(32, 7, dtype=torch.int64)
    tgt = torch.randint(0, 2000, (32, 7))

    max_len = memory_bank[0].shape[1] \
            if isinstance(memory_bank, list) else memory_bank.shape[1]
    src_len = [5] * 32
    src_len = torch.tensor(src_len)
    print(src_len.shape)
    decoder.init_state(src_len, max_len)
    dec_outs, attns = decoder(tgt, memory_bank=memory_bank, attn_type=ATTEN_TYPE_HYGRA)
    print(dec_outs.shape)