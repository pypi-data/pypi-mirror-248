import torch
import torch.nn as nn
from torch import Tensor
# https://github.com/iamfaith/attentions
from aicmder.torch.transformer import PositionwiseFeedForward, ActivationFunction, ACTIVATION_FUNCTIONS
import numpy as np
from typing import Optional, Tuple
from torch.nn.init import xavier_uniform_


class DotProductAttention(nn.Module):
    """
    Compute the dot products of the query with all values and apply a softmax function to obtain the weights on the values

    input: batch x num_tree x input_len x dim  16,50,10,100 or 16,50,1000
    w_attn: num_tree x 1     50,1

    input x w_attn = 16,50,1000 x 50,1

    ref: https://discuss.pytorch.org/t/what-is-the-difference-between-register-buffer-and-register-parameter-of-nn-module/32723/8

    """

    def __init__(
            self, atten_dim, d_ff=1024, use_ff=True, activation_fn=ActivationFunction.softmax,
            dropout=0.2):
        super(DotProductAttention, self).__init__()
        self.atten_dim = atten_dim
        data = np.random.uniform(0, 1, (self.atten_dim))
        # self.w_attn = torch.tensor(data, requires_grad=True, dtype=torch.float32)
        # using buffer instead
        self.register_buffer('w_attn', torch.tensor(data, requires_grad=True, dtype=torch.float32))

        self.feed_forward = PositionwiseFeedForward(
            self.atten_dim, d_ff=d_ff, dropout=dropout, activation_fn=ActivationFunction.relu) if use_ff else None
        self.activation_fn = activation_fn

    def forward(self, repr: Tensor) -> Tuple[Tensor, Tensor]:

        batch_size, input_len, hidden_dim = repr.size(0), repr.size(1), repr.size(2)

        # (batch_size, tree_num, dim) x (1, tree_num, 1)
        if self.feed_forward is not None:
            temp_w_attn = self.feed_forward(self.w_attn)
        else:
            temp_w_attn = self.w_attn
        aggregated_repr = torch.einsum('aik,bij->aik', [repr, temp_w_attn.reshape(1, -1, 1)])

        # attention_score = aggregated_repr.reshape([batch_size, -1, hidden_dim])
        attention_score = aggregated_repr

        attention_weights = ACTIVATION_FUNCTIONS[self.activation_fn](attention_score, dim=1)

        weighted_average = torch.multiply(repr, attention_weights)
        weighted_average = torch.sum(weighted_average, dim=1)
        return weighted_average, attention_weights

    def update_dropout(self, dropout):
        self.feed_forward.update_dropout(dropout)


class _DotProductAttention(nn.Module):
    """
    Compute the dot products of the query with all values and apply a softmax function to obtain the weights on the values

    input: batch x num_tree x input_len x dim  16,50,10,100
    w_attn: dim x 1   or   input_len x dim     10,100,1
    """

    def __init__(self, hidden_dim):
        super(DotProductAttention, self).__init__()

    def forward(self, repr: Tensor, w_attn: Tensor) -> Tuple[Tensor, Tensor]:
        assert repr.dim() - w_attn.dim() == 2
        batch_size, input_len, hidden_dim = repr.size(0), repr.size(1), repr.size(2)

        flat_shape = list(w_attn.shape)
        flat_shape.insert(0, -1)
        flat_repr = repr.reshape(flat_shape)

        # print(flat_repr.shape, w_attn.shape)
        # aggregated_repr = torch.einsum('ij,jkl->ikl', w_attn, flat_repr)
        aggregated_repr = torch.matmul(flat_repr, w_attn)
        attention_score = aggregated_repr.reshape([-1, input_len, 1])

        attention_weights = F.softmax(attention_score, dim=1)

        weighted_average = torch.multiply(repr, attention_weights)
        weighted_average = torch.sum(weighted_average, dim=1)
        return weighted_average, attention_weights


class EmbeddingAttentionLayer(nn.Module):
    def __init__(self, dim: int, activation_fn=ActivationFunction.softmax) -> None:
        super().__init__()
        self.dim = dim
        self.activation_fn = activation_fn
        self.attention = torch.randn(1, dim)
        self.attention = nn.Parameter(self.attention)
        # def _reset_module_parameters(self, module):
        # print(self.attention[:20])
        # for p in self.attention:
        #     if p.dim() > 1:
        #         xavier_uniform_(p)
        # print(self.attention[:20])

    def compute_weights(self, embedded: torch.Tensor) -> torch.Tensor:
        unnormalized_weights = embedded.matmul(self.attention.t())
        attention_weights = ACTIVATION_FUNCTIONS[self.activation_fn](unnormalized_weights, dim=1)
        return attention_weights

    def forward(self, embedded: torch.Tensor) -> torch.Tensor:
        attention_weights = self.compute_weights(embedded)
        # print("forward", attention_weights.shape, embedded.shape)
        weighted = torch.matmul(attention_weights.transpose(1, 2), embedded)
        return weighted


# class ModelDevice:
#     def __init__(self, *args, **kwargs):
#         if 'device' in kwargs:
#             self.device = kwargs['device']
#             for k in args:
#                 k = k.to(self.device)

#     def __enter__(self):
#         pass

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass


if __name__ == "__main__":

    import numpy as np
    from aicmder.torch import init_seeds
    init_seeds()
    hidden_size = 100
    num_tree = 50
    path_len = 10
    from aicmder.benchmark import model_info

    #                                     N   C         H   W
    memory_bank = torch.randint(0, 2000, (16, num_tree, path_len, hidden_size), dtype=torch.float64)
    dot_attn = DotProductAttention(atten_dim=num_tree, use_ff=False)
    # dot_attn.to(device='cpu')
    model_info(dot_attn)
    print(memory_bank.shape)
    memory_bank = memory_bank.reshape([memory_bank.size(0), memory_bank.size(1), -1]).contiguous()
    # memory_bank.view([memory_bank.size(0), memory_bank.size(1), -1])
    print(memory_bank.shape)
    # print(memory_bank.shape, memory_bank.size())
    out, _ = dot_attn(memory_bank)
    print(out.shape)

    ea = EmbeddingAttentionLayer(hidden_size)
    model_info(ea)

    test_input = torch.randint(0, 2000, (num_tree, path_len, hidden_size), dtype=torch.float32)
    out = ea(test_input)
    print(test_input.shape, out.shape)
    # print(out)

    test_input = torch.randint(0, 2000, (num_tree, path_len + 20, hidden_size), dtype=torch.float32)
    from aicmder.torch import cpu, gpu
    
    def f(ea, test_input):
        ea.to(gpu())
        # test_input.device = gpu()
        test_input.to(gpu())
        print(id(test_input), test_input.device)
    print(id(test_input), test_input.device)
    # test_input = test_input.to(gpu())
    # f(ea, test_input)
    # with ModelDevice(ea, test_input, device=gpu()):
    print(test_input.device, id(test_input)) #, ea.device)
    out = ea(test_input)
    print(test_input.shape, out.shape, out.device, test_input.device)
