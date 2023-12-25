# src: https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/decoders/decoder.py
from aicmder.torch.transformer.base_model import DecoderBase
import torch.nn as nn
from aicmder.torch.transformer.misc import aeq
from aicmder.torch.transformer.state import RNNDecoderState
import torch
from aicmder.torch.transformer.global_attention import GlobalAttention

def rnn_factory(rnn_type, **kwargs):
    """ rnn factory, Use pytorch version when available. """
    no_pack_padded_seq = False
    if rnn_type == "SRU":
        # SRU doesn't support PackedSequence.
        no_pack_padded_seq = True
        # rnn = onmt.models.sru.SRU(**kwargs)
        raise NotImplementedError("Not implemented yet!")
    else:
        rnn = getattr(nn, rnn_type)(**kwargs)
    return rnn, no_pack_padded_seq


# many part of the codes are copied from OpenNMT-Py sources
class RNNDecoderBase(nn.Module):
    """
    Base recurrent attention-based decoder class.

    .. mermaid::
       graph BT
          A[Input]
          subgraph RNN
             C[Pos 1]
             D[Pos 2]
             E[Pos N]
          end
          G[Decoder State]
          H[Decoder State]
          I[Outputs]
          F[Memory_Bank]
          A--emb-->C
          A--emb-->D
          A--emb-->E
          H-->C
          C-- attn --- F
          D-- attn --- F
          E-- attn --- F
          C-->I
          D-->I
          E-->I
          E-->G
          F---I

    Args:
       rnn_type (:obj:`str`):
          style of recurrent unit to use, one of [LSTM, GRU]
       bidirectional (bool) : use with a bidirectional encoder
       num_layers (int) : number of stacked layers
       hidden_size (int) : hidden size of each layer
       attn_type (str) : see :obj:`nqa.modules.GlobalAttention`
       dropout (float) : dropout value for :obj:`nn.Dropout`
    """

    def __init__(self,
                 input_size,
                 bidirectional_encoder,
                 num_layers,
                 hidden_size,
                 rnn_type="LSTM",
                 attn_type='general',
                 coverage_attn=False,
                 copy_attn=False,
                 reuse_copy_attn=False,
                 dropout=0.0):

        super(RNNDecoderBase, self).__init__()

        # Basic attributes.
        self.decoder_type = 'rnn'
        self.bidirectional_encoder = bidirectional_encoder
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.dropout = nn.Dropout(dropout)
        self.input_size = input_size
        self.attn_type = attn_type

        # Build the RNN.
        kwargs = {'input_size': input_size,
                  'hidden_size': hidden_size,
                  'num_layers': num_layers,
                  'dropout': dropout,
                  'batch_first': True}
        self.rnn = getattr(nn, rnn_type)(**kwargs)

        # Set up the standard attention.
        self._coverage = coverage_attn
        self.attn = None
        if self.attn_type:
            self.attn = GlobalAttention(
                hidden_size, coverage=coverage_attn,
                attn_type=self.attn_type
            )
        else:
            assert not self._coverage
            if copy_attn and reuse_copy_attn:
                raise RuntimeError('Attn is turned off, so reuse_copy_attn flag must be false')

        # Set up a separated copy attention layer, if needed.
        self._copy = copy_attn
        self._reuse_copy_attn = reuse_copy_attn
        self.copy_attn = None
        if copy_attn and not reuse_copy_attn:
            self.copy_attn = GlobalAttention(
                hidden_size, attn_type=self.attn_type
            )

    def count_parameters(self):
        params = list(self.rnn.parameters())
        if self.attn is not None:
            params = params + list(self.attn.parameters())
        if self.copy_attn is not None:
            params = params + list(self.copy_attn.parameters())
        return sum(p.numel() for p in params if p.requires_grad)

    def forward(self, tgt, memory_bank, state=None, memory_lengths=None, encoder_final=None):
        """
        Args:
            tgt (`LongTensor`): sequences of padded tokens
                 `[batch x tgt_len x nfeats]`.
            memory_bank (`FloatTensor`): vectors from the encoder
                 `[batch x src_len x hidden]`.
            state (:obj:`onmt.models.DecoderState`):
                 decoder state object to initialize the decoder
            memory_lengths (`LongTensor`): the padded source lengths
                `[batch]`.
        Returns:
            (`FloatTensor`,:obj:`onmt.Models.DecoderState`,`FloatTensor`):
                * decoder_outputs: output from the decoder (after attn)
                         `[batch x tgt_len x hidden]`.
                * decoder_state: final hidden state from the decoder
                * attns: distribution over src at each tgt
                        `[batch x tgt_len x src_len]`.
        """
        assert state is not None or encoder_final is not None
        if encoder_final is not None and state is None:
            state = self.init_decoder_state(encoder_final)
        # Check
        assert isinstance(state, RNNDecoderState)
        # tgt.size() returns tgt length and batch
        tgt_batch, _, _ = tgt.size()
        if self.attn is not None:
            memory_batch, _, _ = memory_bank.size()
            aeq(tgt_batch, memory_batch)
        # END

        # Run the forward pass of the RNN.
        decoder_final, decoder_outputs, attns = self._run_forward_pass(
            tgt, memory_bank, state, memory_lengths=memory_lengths)

        coverage = None
        if "coverage" in attns:
            coverage = attns["coverage"]
        # Update the state with the result.
        state.update_state(decoder_final, coverage)

        return decoder_outputs, state, attns

    def init_decoder_state(self, encoder_final):
        """ Init decoder state with last state of the encoder """

        def _fix_enc_hidden(hidden):
            # The encoder hidden is  (layers*directions) x batch x dim.
            # We need to convert it to layers x batch x (directions*dim).
            if self.bidirectional_encoder:
                hidden = torch.cat([hidden[0:hidden.size(0):2],
                                    hidden[1:hidden.size(0):2]], 2)
            return hidden

        if isinstance(encoder_final, tuple):  # LSTM
            return RNNDecoderState(self.hidden_size,
                                   tuple([_fix_enc_hidden(enc_hid)
                                          for enc_hid in encoder_final]))
        else:  # GRU
            return RNNDecoderState(self.hidden_size,
                                   _fix_enc_hidden(encoder_final))


class RNNDecoder(RNNDecoderBase):
    """
    Standard fully batched RNN decoder with attention.
    Faster implementation, uses CuDNN for implementation.
    See :obj:`RNNDecoderBase` for options.
    Based around the approach from
    "Neural Machine Translation By Jointly Learning To Align and Translate"
    :cite:`Bahdanau2015`
    """

    def _run_forward_pass(self, tgt, memory_bank, state, memory_lengths=None):
        """
        Private helper for running the specific RNN forward pass.
        Must be overriden by all subclasses.
        Args:
            tgt (LongTensor): a sequence of input tokens tensors
                                 [batch x len x nfeats].
            memory_bank (FloatTensor): output(tensor sequence) from the encoder
                        RNN of size (batch x src_len x hidden_size).
            state (FloatTensor): hidden state from the encoder RNN for
                                 initializing the decoder.
            memory_lengths (LongTensor): the source memory_bank lengths.
        Returns:
            decoder_final (Tensor): final hidden state from the decoder.
            decoder_outputs (Tensor): output from the decoder (after attn)
                         `[batch x tgt_len x hidden]`.
            attns (Tensor): distribution over src at each tgt
                        `[batch x tgt_len x src_len]`.
        """
        # Initialize local and return variables.
        attns = {}

        emb = tgt
        assert emb.dim() == 3

        coverage = state.coverage

        if isinstance(self.rnn, nn.GRU):
            rnn_output, decoder_final = self.rnn(emb, state.hidden[0])
        else:
            rnn_output, decoder_final = self.rnn(emb, state.hidden)

        # Check
        tgt_batch, tgt_len, _ = tgt.size()
        output_batch, output_len, _ = rnn_output.size()
        aeq(tgt_len, output_len)
        aeq(tgt_batch, output_batch)
        # END

        # Calculate the attention.
        if self.attn is not None:
            decoder_outputs, p_attn, coverage_v = self.attn(
                rnn_output.contiguous(),
                memory_bank,
                memory_lengths=memory_lengths,
                coverage=coverage,
                softmax_weights=False
            )
            attns["std"] = p_attn
        else:
            decoder_outputs = rnn_output.contiguous()

        # Update the coverage attention.
        if self._coverage:
            if coverage_v is None:
                coverage = coverage + p_attn \
                    if coverage is not None else p_attn
            else:
                coverage = coverage + coverage_v \
                    if coverage is not None else coverage_v
            attns["coverage"] = coverage

        decoder_outputs = self.dropout(decoder_outputs)
        # Run the forward pass of the copy attention layer.
        if self._copy and not self._reuse_copy_attn:
            _, copy_attn, _ = self.copy_attn(decoder_outputs,
                                             memory_bank,
                                             memory_lengths=memory_lengths,
                                             softmax_weights=False)
            attns["copy"] = copy_attn
        elif self._copy:
            attns["copy"] = attns["std"]

        return decoder_final, decoder_outputs, attns


if __name__ == "__main__":
    from aicmder.torch import init_seeds
    from aicmder.benchmark import model_info
    init_seeds(0)

    rnn_type = "LSTM"
    bidirection = True
    num_layers = 6
    hidden_size = 200
    input_size = 300
    rnn = RNNDecoder(rnn_type=rnn_type, bidirectional_encoder=bidirection, num_layers=num_layers,
                    #  attn_type=None,
                     hidden_size=hidden_size, coverage_attn=False, reuse_copy_attn=False, dropout=0.2, input_size=input_size)

    print(rnn)

    batch_size = 32
    max_len = 7
    # input
    tgt = torch.rand(batch_size, max_len, input_size, dtype=torch.float32)

    # memory
    memory_bank = torch.rand(batch_size, 5, hidden_size, dtype=torch.float32)
    memory_lengths = torch.Tensor([5] * batch_size)

    hidden = (torch.rand(num_layers * 2, batch_size, 100), torch.rand(num_layers * 2, batch_size, 100))
    dec_state = rnn.init_decoder_state(hidden)

    decoder_outputs, state, attns = rnn(tgt,
                                    memory_bank,
                                    # state=dec_state,
                                    encoder_final=hidden,
                                    memory_lengths=memory_lengths)

    print(decoder_outputs.shape, attns['std'].shape if 'std' in attns else None)
    # model_info(rnn, verbose=True)
