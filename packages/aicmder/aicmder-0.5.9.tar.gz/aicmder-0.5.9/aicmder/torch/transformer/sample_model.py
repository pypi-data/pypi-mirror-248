import torch
import torch.nn as nn
try:
    from encoder import TransformerEncoder
    from decoder import TransformerDecoder
    from embedding import Embeddings, PADDING_INDEX, _position_encoding_default, _position_encoding_absolute
    from multi_headed_attn import MultiHeadedAttention, ATTEN_TYPE_SELF, ATTEN_TYPE_HYGRA
except:
    from aicmder.torch.transformer import TransformerEncoder, TransformerDecoder, Embeddings, PADDING_INDEX, ATTEN_TYPE_SELF, _position_encoding_default, _position_encoding_absolute
from aicmder.torch.dist_model import Trainable
from torch.nn import functional as F
from torch import Tensor
from typing import Optional, Any, Union, Callable
from torch.nn.init import xavier_uniform_


_attn_type = ATTEN_TYPE_SELF
# _attn_type = ATTEN_TYPE_HYGRA 
class TransformerSample(nn.Module):

    def __init__(self, args):

        super(TransformerSample, self).__init__()

        if "src_word_vocab_size" in args:
            source_embeddings = Embeddings(args.d_model, args.src_word_vocab_size, PADDING_INDEX, position_encoding=_position_encoding_default)
        else:
            source_embeddings = None

        num_head = args.num_head
        d_ff = args.d_ff
        num_layer = args.nlayers
        self.encoder = TransformerEncoder(
            num_head, args.d_model, args.dropout, args.max_relative_positions, d_ff, embeddings=source_embeddings, num_layers=num_layer, attn_type=_attn_type)
       
        if "tgt_word_vocab_size" in args: 
            target_embeddings = Embeddings(args.d_model, args.tgt_word_vocab_size, PADDING_INDEX, position_encoding=_position_encoding_default) 
        else:
            target_embeddings = None
            
        self.decoder = TransformerDecoder(
            num_layers=num_layer,
            d_model=args.d_model,
            heads=num_head,
            d_ff=d_ff,
            copy_attn=False,
            embeddings=target_embeddings,
            dropout=args.dropout
        )

        # layer_norm_eps = 1e-5
        # batch_first = False
        # norm_first = False
        # factory_kwargs = {'device': None, 'dtype': None}
        # activation = F.relu
        # decoder_layer = nn.TransformerDecoderLayer(args.d_model, num_head, d_ff, args.dropout,
        #                                         activation, layer_norm_eps, batch_first, norm_first,
        #                                         **factory_kwargs)
        # decoder_norm = nn.LayerNorm(args.d_model, eps=layer_norm_eps, **factory_kwargs)
        # self.decoder = nn.TransformerDecoder(decoder_layer, num_layer, decoder_norm)
        
        self._reset_parameters()



    # def forward(self, src_input, tgt: Tensor, src_mask: Optional[Tensor] = None, tgt_mask: Optional[Tensor] = None,
    #             memory_mask: Optional[Tensor] = None, src_key_padding_mask: Optional[Tensor] = None,
    #             tgt_key_padding_mask: Optional[Tensor] = None, memory_key_padding_mask: Optional[Tensor] = None) -> Tensor:

    def forward(self, src_input, tgt_input, src_mask=None, tgt_pad_mask=None):
        memory_bank = self.encoder(src_input.float(), mask=src_mask)
        max_mem_len = memory_bank[0].shape[1] \
            if isinstance(memory_bank, list) else memory_bank.shape[1]
        memory_len = torch.tensor([src_input.size(1) for i in range(src_input.size(0))], device=memory_bank.device, dtype=torch.long)
        self.decoder.init_state(memory_len, max_mem_len)
        dec_outs, attns = self.decoder(tgt_input.float(), memory_bank=memory_bank, src_pad_mask=src_mask, tgt_pad_mask=tgt_pad_mask, attn_type=_attn_type)
        return dec_outs, attns


        # memory_bank = self.encoder(src_input.float())
        # output = self.decoder(tgt, memory_bank, tgt_mask=tgt_mask, memory_mask=memory_mask,
        #                       tgt_key_padding_mask=tgt_key_padding_mask,
        #                       memory_key_padding_mask=memory_key_padding_mask)
        # return output


    def _reset_parameters(self):
        r"""Initiate parameters in the transformer model."""

        for p in self.parameters():
            if p.dim() > 1:
                xavier_uniform_(p)

if __name__ == "__main__":
    trainable = Trainable(bs=32)
    args = dict()
    args["d_model"] = 512
    # args["src_word_vocab_size"] = 184866
    # args["tgt_word_vocab_size"] = 184866 
    args["num_head"] = 8
    args["dropout"] = 0.2
    args["d_ff"] = 2048
    args["max_relative_positions"] = 32
    args["nlayers"] = 1
    from aicmder.utils import AttrDict
    model = TransformerSample(AttrDict(args))
    trainable.on_pretrain_routine_start(model, verbose=True)
    


