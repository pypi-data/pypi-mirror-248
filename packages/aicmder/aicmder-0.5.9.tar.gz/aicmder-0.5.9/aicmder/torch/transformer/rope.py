import torch
import torch.nn as nn


class RotaryEmbedding(nn.Module):
    def __init__(self, dim, original_impl=False, device=None, dtype=None):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2, device=device).to(dtype=dtype) / dim))
        self.register_buffer("inv_freq", inv_freq)
        self.dim = dim
        self.original_impl = original_impl

    def forward_impl(
            self, seq_len: int, n_elem: int, dtype: torch.dtype, device: torch.device, base: int = 10000
    ):
        """Enhanced Transformer with Rotary Position Embedding.

        Derived from: https://github.com/labmlai/annotated_deep_learning_paper_implementations/blob/master/labml_nn/
        transformers/rope/__init__.py. MIT License:
        https://github.com/labmlai/annotated_deep_learning_paper_implementations/blob/master/license.
        """
        # $\Theta = {\theta_i = 10000^{\frac{2(i-1)}{d}}, i \in [1, 2, ..., \frac{d}{2}]}$
        theta = 1.0 / (base ** (torch.arange(0, n_elem, 2, dtype=dtype, device=device) / n_elem))

        # Create position indexes `[0, 1, ..., seq_len - 1]`
        seq_idx = torch.arange(seq_len, dtype=dtype, device=device)

        # Calculate the product of position index and $\theta_i$
        idx_theta = torch.outer(seq_idx, theta).float()

        cache = torch.stack([torch.cos(idx_theta), torch.sin(idx_theta)], dim=-1)

        # this is to mimic the behaviour of complex32, else we will get different results
        if dtype in (torch.float16, torch.bfloat16, torch.int8):
            cache = cache.bfloat16() if dtype == torch.bfloat16 else cache.half()
        return cache

    def forward(self, max_seq_len, offset=0):
        return self.forward_impl(
            max_seq_len, self.dim, dtype=self.inv_freq.dtype, device=self.inv_freq.device
        )


@torch.jit.script
def apply_rotary_pos_emb(x: torch.Tensor, rope_cache: torch.Tensor) -> torch.Tensor:
    # x: [sq, b, np, hn]
    sq, b, np, hn = x.size(0), x.size(1), x.size(2), x.size(3)
    rot_dim = rope_cache.shape[-2] * 2
    x, x_pass = x[..., :rot_dim], x[..., rot_dim:]
    # truncate to support variable sizes
    rope_cache = rope_cache[:sq]
    xshaped = x.reshape(sq, -1, np, rot_dim // 2, 2)
    rope_cache = rope_cache.view(sq, -1, 1, xshaped.size(3), 2)
    x_out2 = torch.stack(
        [
            xshaped[..., 0] * rope_cache[..., 0] - xshaped[..., 1] * rope_cache[..., 1],
            xshaped[..., 1] * rope_cache[..., 0] + xshaped[..., 0] * rope_cache[..., 1],
        ],
        -1,
    )
    x_out2 = x_out2.flatten(3)
    return torch.cat((x_out2, x_pass), dim=-1)


if __name__ == "__main__":
    config = {
        "_name_or_path": "THUDM/chatglm2-6b",
        "model_type": "chatglm",
        "architectures": [
            "ChatGLMModel"
        ],
        "auto_map": {
            "AutoConfig": "configuration_chatglm.ChatGLMConfig",
            "AutoModel": "modeling_chatglm.ChatGLMForConditionalGeneration",
            "AutoModelForSeq2SeqLM": "modeling_chatglm.ChatGLMForConditionalGeneration"
        },
        "add_bias_linear": False,
        "add_qkv_bias": True,
        "apply_query_key_layer_scaling": True,
        "apply_residual_connection_post_layernorm": False,
        "attention_dropout": 0.0,
        "attention_softmax_in_fp32": True,
        "bias_dropout_fusion": True,
        "ffn_hidden_size": 13696,
        "fp32_residual_connection": False,
        "hidden_dropout": 0.0,
        "hidden_size": 4096,
        "kv_channels": 128,
        "layernorm_epsilon": 1e-05,
        "multi_query_attention": True,
        "multi_query_group_num": 2,
        "num_attention_heads": 32,
        "num_layers": 28,
        "original_rope": True,
        "padded_vocab_size": 65024,
        "post_layer_norm": True,
        "rmsnorm": True,
        "seq_length": 32768,
        "use_cache": True,
        "torch_dtype": "float16",
        "transformers_version": "4.27.1",
        "tie_word_embeddings": False,
        "eos_token_id": 2,
        "pad_token_id": 0
    }
    from aicmder.utils import AttrDict
    config = AttrDict(config)
    rotary_dim = (config.hidden_size // config.num_attention_heads
                  if config.kv_channels is None else config.kv_channels)
    
    torch_dtype = getattr(torch, config.torch_dtype)
    print(rotary_dim, torch_dtype)
    device = torch.device("cuda:0")
    rotary_pos_emb = RotaryEmbedding(
        rotary_dim // 2, original_impl=config.original_rope, device=device, dtype=torch_dtype)

    seq_length = 10
    cache = rotary_pos_emb(seq_length)
    print(cache, cache.shape)
