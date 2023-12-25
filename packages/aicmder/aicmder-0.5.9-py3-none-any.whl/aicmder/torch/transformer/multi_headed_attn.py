# src: https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/modules/multi_headed_attn.py
""" Multi-Head Attention module """
import math
import torch
import torch.nn as nn

from aicmder.torch.transformer.misc import generate_relative_positions_matrix,\
                            relative_matmul
# from onmt.utils.misc import aeq

from torch.nn.init import xavier_uniform_


ATTEN_TYPE_SELF = "self"
ATTEN_TYPE_HYGRA = "hydra"


class MultiHeadedAttention(nn.Module):
    """Multi-Head Attention module from "Attention is All You Need"
    :cite:`DBLP:journals/corr/VaswaniSPUJGKP17`.
    Similar to standard `dot` attention but uses
    multiple attention distributions simulataneously
    to select relevant items.
    .. mermaid::
       graph BT
          A[key]
          B[value]
          C[query]
          O[output]
          subgraph Attn
            D[Attn 1]
            E[Attn 2]
            F[Attn N]
          end
          A --> D
          C --> D
          A --> E
          C --> E
          A --> F
          C --> F
          D --> O
          E --> O
          F --> O
          B --> O
    Also includes several additional tricks.
    Args:
       head_count (int): number of parallel heads
       model_dim (int): the dimension of keys/values/queries,
           must be divisible by head_count
       dropout (float): dropout parameter
    """

    def __init__(self, head_count, model_dim, dropout=0.1,
                 max_relative_positions=0, use_neg_dist=True):
        assert model_dim % head_count == 0
        self.dim_per_head = model_dim // head_count
        self.model_dim = model_dim

        super(MultiHeadedAttention, self).__init__()
        self.head_count = head_count

        self.linear_keys = nn.Linear(model_dim,
                                     head_count * self.dim_per_head)
        self.linear_values = nn.Linear(model_dim,
                                       head_count * self.dim_per_head)
        self.linear_query = nn.Linear(model_dim,
                                      head_count * self.dim_per_head)
        self.softmax = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(dropout)
        self.final_linear = nn.Linear(model_dim, model_dim)

        self.max_relative_positions = max_relative_positions

        self.use_neg_dist = use_neg_dist
    
        if max_relative_positions > 0:
            vocab_size = max_relative_positions * 2 + 1 \
                if self.use_neg_dist else max_relative_positions + 1
            self.relative_positions_embeddings = nn.Embedding(
                vocab_size, self.dim_per_head)
        self._reset_parameters()

    def _reset_module_parameters(self, module):
        for p in module.parameters():
            if p.dim() > 1:
                xavier_uniform_(p)

    def _reset_parameters(self):
        self._reset_module_parameters(self.linear_keys)
        self._reset_module_parameters(self.linear_values)
        self._reset_module_parameters(self.linear_query)


    def forward(self, key, value, query, mask=None,
                layer_cache=None, attn_type=None):
        """
        Compute the context vector and the attention vectors.
        Args:
           key (FloatTensor): set of `key_len`
               key vectors ``(batch, key_len, dim)``
           value (FloatTensor): set of `key_len`
               value vectors ``(batch, key_len, dim)``
           query (FloatTensor): set of `query_len`
               query vectors  ``(batch, query_len, dim)``
           mask: binary mask 1/0 indicating which keys have
               zero / non-zero attention ``(batch, query_len, key_len)``
        Returns:
           (FloatTensor, FloatTensor):
           * output context vectors ``(batch, query_len, dim)``
           * Attention vector in heads ``(batch, head, query_len, key_len)``.
        """

        # CHECKS
        # batch, k_len, d = key.size()
        # batch_, k_len_, d_ = value.size()
        # aeq(batch, batch_)
        # aeq(k_len, k_len_)
        # aeq(d, d_)
        # batch_, q_len, d_ = query.size()
        # aeq(batch, batch_)
        # aeq(d, d_)
        # aeq(self.model_dim % 8, 0)
        # if mask is not None:
        #    batch_, q_len_, k_len_ = mask.size()
        #    aeq(batch_, batch)
        #    aeq(k_len_, k_len)
        #    aeq(q_len_ == q_len)
        # END CHECKS

        batch_size = key.size(0)
        dim_per_head = self.dim_per_head
        head_count = self.head_count
        key_len = key.size(1)
        query_len = query.size(1)
        
        attn = None

        def shape(x):
            """Projection."""
            return x.view(batch_size, -1, head_count, dim_per_head) \
                .transpose(1, 2)

        def unshape(x):
            """Compute context."""
            return x.transpose(1, 2).contiguous() \
                    .view(batch_size, -1, head_count * dim_per_head)

        # 1) Project key, value, and query.
        if layer_cache is not None:
            if attn_type == ATTEN_TYPE_SELF:
                query, key, value = self.linear_query(query),\
                                    self.linear_keys(query),\
                                    self.linear_values(query)
                key = shape(key)
                value = shape(value)
                if layer_cache["self_keys"] is not None:
                    key = torch.cat(
                        (layer_cache["self_keys"], key),
                        dim=2)
                if layer_cache["self_values"] is not None:
                    value = torch.cat(
                        (layer_cache["self_values"], value),
                        dim=2)
                layer_cache["self_keys"] = key
                layer_cache["self_values"] = value
            elif attn_type == "context":
                query = self.linear_query(query)
                if layer_cache["memory_keys"] is None:
                    key, value = self.linear_keys(key),\
                                 self.linear_values(value)
                    key = shape(key)
                    value = shape(value)
                else:
                    key, value = layer_cache["memory_keys"],\
                               layer_cache["memory_values"]
                layer_cache["memory_keys"] = key
                layer_cache["memory_values"] = value
        else:
            key = self.linear_keys(key)
            value = self.linear_values(value)
            query = self.linear_query(query)
            key = shape(key)
            value = shape(value)

        if self.max_relative_positions > 0 and attn_type == ATTEN_TYPE_SELF:
            key_len = key.size(2)
            # 1 or key_len x key_len
            relative_positions_matrix = generate_relative_positions_matrix(
                key_len, self.max_relative_positions,
                use_neg_dist=self.use_neg_dist,
                cache=True if layer_cache is not None else False)
            #  1 or key_len x key_len x dim_per_head
            relations_keys = self.relative_positions_embeddings(
                relative_positions_matrix.to(key.device))
            #  1 or key_len x key_len x dim_per_head
            relations_values = self.relative_positions_embeddings(
                relative_positions_matrix.to(key.device))

        query = shape(query)

        key_len = key.size(2)
        query_len = query.size(2)

        if attn_type == ATTEN_TYPE_SELF:
            # 2) Calculate and scale scores.
            query = query / math.sqrt(dim_per_head)
            # batch x num_heads x query_len x key_len
            query_key = torch.matmul(query, key.transpose(2, 3))

            if self.max_relative_positions > 0 and attn_type == ATTEN_TYPE_SELF:
                scores = query_key + relative_matmul(query, relations_keys, True)
            else:
                scores = query_key
            scores = scores.float()

            if mask is not None:
                if len(mask.size()) == 3:
                    mask = mask.unsqueeze(1)  # [B, 1, 1, T_values]
                if len(mask.size()) == 2:
                    mask = mask.unsqueeze(1)
                    mask = mask.unsqueeze(1)  # [B, 1, 1, T_values]
                scores = scores.masked_fill(mask, float("-inf"))
                # scores = scores.masked_fill(mask, -1e18)

            # 3) Apply attention dropout and compute context vectors.
            attn = self.softmax(scores).to(query.dtype)

            if self.training:
                drop_attn = self.dropout(attn)
            else:
                drop_attn = attn

            context_original = torch.matmul(drop_attn, value)
        elif attn_type == ATTEN_TYPE_HYGRA:
            ##################### hydra attention
            ##### TODO: does it need dropout?
            q = query / query.norm(dim=-1, keepdim=True)
            k = key / key.norm(dim=-1, keepdim=True)
                
            ###### origin  
            # ref: https://arxiv.org/pdf/2209.07484.pdf
            # kv = (k * value).sum(dim=-2, keepdim=True)
            # context_original = q * kv
            ###########################
           
            
            qk = torch.matmul(q, k.transpose(2, 3)) 
        
            if self.max_relative_positions > 0 and attn_type == ATTEN_TYPE_SELF:
                scores = qk + relative_matmul(q, relations_keys, True)
            else:
                scores = qk
            scores = scores.float()
        
            if mask is not None:
                if len(mask.size()) == 3:
                    mask = mask.unsqueeze(1)  # [B, 1, 1, T_values]
                if len(mask.size()) == 2:
                    mask = mask.unsqueeze(1)
                    mask = mask.unsqueeze(1)  # [B, 1, 1, T_values]
                scores = scores.masked_fill(mask, float("-inf"))
                # scores = scores.masked_fill(mask, -1e18)

            # 3) Apply attention dropout and compute context vectors.
            attn = self.softmax(scores).to(query.dtype)

            if self.training:
                drop_attn = self.dropout(attn)
            else:
                drop_attn = attn

            context_original = torch.matmul(drop_attn, value)
            
        else:
            assert "Atten_type[{}] is not supported".format(attn_type)

        if self.max_relative_positions > 0 and attn_type == ATTEN_TYPE_SELF:
            context = unshape(context_original
                              + relative_matmul(drop_attn,
                                                relations_values,
                                                False))
        else:
            context = unshape(context_original)

        output = self.final_linear(context)
        # CHECK
        # batch_, q_len_, d_ = output.size()
        # aeq(q_len, q_len_)
        # aeq(batch, batch_)
        # aeq(d, d_)

        # Return multi-head attn
        if attn is not None:
            attns = attn \
                .view(batch_size, head_count,
                    query_len, key_len)
            
            # attn_per_head = [attn.squeeze(1)
                        #  for attn in attn.chunk(head_count, dim=1)]
            
            # print('---', len(attn_per_head),(attn_per_head[0]).shape, attns.shape)
        else:
            attns = None

        return output, attns

    def update_dropout(self, dropout):
        self.dropout.p = dropout

        
if __name__ == "__main__":
    from aicmder.torch import init_seeds
    from misc import sequence_mask
    init_seeds(0)
    heads = 2
    d_model = 4
    dropout = 0
    max_relative_positions = 32
    use_neg_dist = True
    attention = MultiHeadedAttention(head_count=heads, model_dim=d_model,
                                            dropout=dropout,
                                            max_relative_positions=max_relative_positions,
                                            use_neg_dist=use_neg_dist)

    # inputs = torch.randint(0, 20000, (32, 5, d_model))
    N = 3
    inputs = torch.rand(N, 2, d_model, dtype=torch.float32)
    code_len = torch.zeros(N, dtype=torch.long)
    code_len[:] = 2
    print(inputs.shape)
    mask = None if code_len is None else \
            ~sequence_mask(code_len, inputs.shape[1]).unsqueeze(1)
    # context, attn_per_head = attention(inputs, inputs, inputs, mask=mask, attn_type=ATTEN_TYPE_SELF)
    context, attn_per_head = attention(inputs, inputs, inputs, mask=mask, attn_type=ATTEN_TYPE_HYGRA)
    print(type(context), type(attn_per_head))
    print(context.shape, attn_per_head)
    print(torch.nn.MultiheadAttention)
    # import torch.nn as nn
    # import torch

    embed_dim = 3
    num_heads = 1

    x = [
        [1, 0, 1], # Input 1
        [0, 2, 0], # Input 2
        [1, 1, 1] # Input 3
    ]

    x = torch.tensor(x, dtype=torch.float32)

    w_key = [
        [0, 0, 1],
        [1, 1, 0],
        # [0, 1, 0],
        [1, 1, 0]
    ]

    w_query = [
        [1, 0, 1],
        [1, 0, 0],
        # [0, 0, 1],
        [0, 1, 1]
    ]

    w_value = [
        [0 ,0 ,0],
        [1 ,0 ,1],
        # [1 ,0 ,0],
        [0 ,1 ,0]
    ]

    w_key   = torch.tensor(w_key   , dtype=torch.float32)
    w_query = torch.tensor(w_query , dtype=torch.float32)
    w_value = torch.tensor(w_value , dtype=torch.float32)

    # The input to the MultiheadAttention layer is of shape (S,N,E) where S is the sequence length,
    # N is the batch size and E is the embedding dimension. In this example we have only one input vector,
    # so we need to add an extra dimension for the batch size.

    x = x.unsqueeze(1) # shape (3 ,4) -> (3 ,1 ,4)

    # The weights for the projection matrices are stored as parameters of the MultiheadAttention layer,
    # so we need to create an instance of this layer and assign our weights to it.

    multihead_attn = nn.MultiheadAttention(embed_dim=embed_dim,num_heads=num_heads)

    project_weight = torch.cat([w_query,w_key,w_value],dim=0)
    print(project_weight.shape, w_query.shape, w_key.shape, w_value.shape, multihead_attn.in_proj_weight.data.shape)
    multihead_attn.in_proj_weight.data.copy_(project_weight) # shape (12 ,4)

    # We can now call the forward method of the layer with our input vector as query,key and value.

    print(x.shape)
    attn_output,_=multihead_attn(x,x,x)

    print(attn_output.squeeze(1))