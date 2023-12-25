# src: https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/encoders/rnn_encoder.py
"""Define RNN-based encoders."""
from __future__ import division
import warnings
warnings.filterwarnings("ignore")
import torch
import torch.nn as nn
import torch.nn.functional as F

from aicmder.torch.transformer.base_model import EncoderBase
from torch.nn.utils.rnn import pack_padded_sequence as pack
from torch.nn.utils.rnn import pad_packed_sequence as unpack
from aicmder.torch.transformer.misc import aeq
from aicmder.torch import HyperParameters, Module
from aicmder.torch.transformer.attention import DotProductAttention

class RNNEncoder(EncoderBase):
    """ A generic recurrent neural network encoder.
    Args:
       rnn_type (:obj:`str`):
          style of recurrent unit to use, one of [RNN, LSTM, GRU, SRU]
       bidirectional (bool) : use a bidirectional RNN
       num_layers (int) : number of stacked layers
       hidden_size (int) : hidden size of each layer
       dropout (float) : dropout value for :obj:`nn.Dropout`
    """

    def __init__(self,
                 hidden_size=100,
                 num_layers=6,
                 rnn_type="LSTM",
                 bidirectional=True,
                 input_size=None,
                 embeddings=None,
                 dropout=0.2,
                 use_bridge=False,
                 use_last=True):
        super(RNNEncoder, self).__init__()

        num_directions = 2 if bidirectional else 1
        assert hidden_size % num_directions == 0
        self.hidden_size = hidden_size
        hidden_size = hidden_size // num_directions

        self.embeddings = embeddings
        assert embeddings is not None or input_size is not None
        if input_size is None:
            input_size = embeddings.embedding_size

        # Saves preferences for layer
        self.nlayers = num_layers
        self.use_last = use_last

        self.rnns = nn.ModuleList()
        for i in range(self.nlayers):
            input_size = input_size if i == 0 else hidden_size * num_directions
            kwargs = {'input_size': input_size,
                      'hidden_size': hidden_size,
                      'num_layers': 1,
                      'bidirectional': bidirectional,
                      'batch_first': True}
            rnn = getattr(nn, rnn_type)(**kwargs)
            self.rnns.append(rnn)

        self.dropout = nn.Dropout(dropout)
        # Initialize the bridge layer
        self.use_bridge = use_bridge
        if self.use_bridge:
            nl = 1 if self.use_last else num_layers
            self._initialize_bridge(rnn_type, hidden_size, nl)

    def count_parameters(self):
        params = list(self.rnns.parameters())
        if self.use_bridge:
            params = params + list(self.bridge.parameters())
        return sum(p.numel() for p in params if p.requires_grad)

    def forward(self, emb, lengths=None):
        "See :obj:`EncoderBase.forward()`"
        self._check_args(emb, lengths)

        if self.embeddings is not None:
            emb = self.embeddings(emb)

        packed_emb = emb
        if lengths is not None:
            # Lengths data is wrapped inside a Tensor.
            lengths, indices = torch.sort(lengths, 0, True)  # Sort by length (keep idx)
            packed_emb = pack(packed_emb[indices], lengths.tolist(), batch_first=True)
            _, _indices = torch.sort(indices, 0)  # Un-sort by length

        memory_bank, encoder_final = [], {'h_n': [], 'c_n': []}
        for i in range(self.nlayers):
            if i != 0:
                packed_emb = self.dropout(packed_emb)
                if lengths is not None:
                    packed_emb = pack(packed_emb, lengths.tolist(), batch_first=True)

            packed_emb, states = self.rnns[i](packed_emb)
            if isinstance(states, tuple):
                h_n, c_n = states
                encoder_final['c_n'].append(c_n)
            else:
                h_n = states
            encoder_final['h_n'].append(h_n)

            packed_emb = unpack(packed_emb, batch_first=True)[0] if lengths is not None else packed_emb
            if not self.use_last or i == self.nlayers - 1:
                memory_bank += [packed_emb[_indices]] if lengths is not None else [packed_emb]

        assert len(encoder_final['h_n']) != 0
        if self.use_last:
            memory_bank = memory_bank[-1]
            if len(encoder_final['c_n']) == 0:
                encoder_final = encoder_final['h_n'][-1]
            else:
                encoder_final = encoder_final['h_n'][-1], encoder_final['c_n'][-1]
        else:
            memory_bank = torch.cat(memory_bank, dim=2)
            if len(encoder_final['c_n']) == 0:
                encoder_final = torch.cat(encoder_final['h_n'], dim=0)
            else:
                encoder_final = torch.cat(encoder_final['h_n'], dim=0), \
                    torch.cat(encoder_final['c_n'], dim=0)

        if self.use_bridge:
            encoder_final = self._bridge(encoder_final)

        # TODO: Temporary hack is adopted to compatible with DataParallel
        # reference: https://github.com/pytorch/pytorch/issues/1591
        if memory_bank.size(1) < emb.size(1):
            dummy_tensor = torch.zeros(memory_bank.size(0),
                                       emb.size(1) - memory_bank.size(1),
                                       memory_bank.size(2)).type_as(memory_bank)
            memory_bank = torch.cat([memory_bank, dummy_tensor], 1)

        return encoder_final, memory_bank

    def _initialize_bridge(self,
                           rnn_type,
                           hidden_size,
                           num_layers):

        # LSTM has hidden and cell state, other only one
        number_of_states = 2 if rnn_type == "LSTM" else 1
        # Total number of states
        self.total_hidden_dim = hidden_size * num_layers

        # Build a linear layer for each
        self.bridge = nn.ModuleList([nn.Linear(self.total_hidden_dim,
                                               self.total_hidden_dim,
                                               bias=True)
                                     for _ in range(number_of_states)])

    def _bridge(self, hidden):
        """
        Forward hidden state through bridge
        """

        def bottle_hidden(linear, states):
            """
            Transform from 3D to 2D, apply linear and return initial size
            """
            size = states.size()
            result = linear(states.view(-1, self.total_hidden_dim))
            return F.relu(result).view(size)

        if isinstance(hidden, tuple):  # LSTM
            outs = tuple([bottle_hidden(layer, hidden[ix])
                          for ix, layer in enumerate(self.bridge)])
        else:
            outs = bottle_hidden(self.bridge[0], hidden)
        return outs

    def update_dropout(self, dropout):
        self.dropout.p = dropout

################### add attention
class AttnRNNEncoder(Module):

    def __init__(self, *args, use_attn=True, use_ff=False, **kwargs):
        super().__init__()
        self.save_hyperparameters()
        self.encoder = RNNEncoder(**kwargs)
        self.use_attn = use_attn
            
        self.dropout = nn.Dropout(self.dropout)
        # self.hidden_size = kwargs["hidden_size"]
        # self.num_layers = kwargs["num_layers"]

        # print(self.use_attn, self.dropout, self.hidden_size)
        if self.use_attn:
            self.dot_attn = DotProductAttention(atten_dim=self.num_layers, use_ff=use_ff)

    def forward(self, emb, lengths=None):
        # M: batch_size x seq_len x nhidden*nlayers
        hidden, M = self.encoder(emb, lengths=lengths)

        layer_outputs = M.split(self.hidden_size, dim=2)
        if self.use_attn:
            output = torch.stack(layer_outputs, dim=2)
            batchs = []
            for i in range(output.size(0)):
                batch_output, _ = self.dot_attn(output[i])
                batchs.append(batch_output)
                
            M = torch.stack(batchs, dim=0)    
            # print("using attn")
            
        else:
            # print("not using attn")
            M = layer_outputs[-1]
        M = M.split(self.hidden_size, dim=2)[-1]
        M = self.dropout(M)
        return  hidden, M
    # def __init__(self,
    #              args,
    #              input_size):
    #     super(Encoder, self).__init__()
    #     self.encoder = RNNEncoder(args.rnn_type,
    #                               input_size,
    #                               args.bidirection,
    #                               args.nlayers,
    #                               args.nhid,
    #                               args.dropout_rnn,
    #                               use_last=False)
    #     self.hidden_size = args.nhid
    #     self.use_all_enc_layers = args.use_all_enc_layers
    #     if self.use_all_enc_layers:
    #         self.layer_weights = nn.Linear(self.hidden_size, 1,
    #                                        bias=False)
    #     self.dropout = nn.Dropout(p=args.dropout_rnn)

    # def count_parameters(self):
    #     return self.encoder.count_parameters()

    # def forward(self, input, input_len):
    #     # M: batch_size x seq_len x nhid*nlayers
    #     hidden, M = self.encoder(input, input_len)
    #     # M: batch_size x seq_len x nhid
    #     layer_outputs = M.split(self.hidden_size, dim=2)
    #     if self.use_all_enc_layers:
    #         output = torch.stack(layer_outputs, dim=2)  # batch_size x seq_len x nlayers x nhid
    #         layer_scores = self.layer_weights(output).squeeze(3)
    #         layer_scores = f.softmax(layer_scores, dim=-1)
    #         M = torch.matmul(output.transpose(2, 3), layer_scores.unsqueeze(3)).squeeze(3)
    #     else:
    #         M = layer_outputs[-1]
    #     M = M.split(self.hidden_size, dim=2)[-1]
    #     M = self.dropout(M)
    #     return hidden, M


if __name__ == "__main__":
    from aicmder.torch import init_seeds
    init_seeds(0)

    rnn_type = "LSTM"
    input_size = 300
    bidirection = True
    num_layers = 6
    hidden_size = 200
    dropout_rnn = 0.2
    encoder = AttnRNNEncoder(rnn_type,
                         bidirectional=bidirection,
                         hidden_size=hidden_size,
                         num_layers=num_layers,
                         dropout=dropout_rnn,
                         input_size=input_size,
                         use_attn=True,
                         use_last=False)

    max_len = 38
    batch_size = 32
    embs = torch.rand(batch_size, max_len, input_size, dtype=torch.float32)
    lengths = [max_len] * batch_size
    print(lengths, type(lengths))
    lengths = torch.Tensor(lengths)
    # lengths = torch.Tensor([max_len] * batch_size, dtype=torch.int64)
    print(lengths.shape, embs.shape)

    encoder_final, memory_bank = encoder(embs, lengths)
    print(len(encoder_final), memory_bank.shape)

    from aicmder.benchmark import model_info

    model_info(encoder, verbose=True)