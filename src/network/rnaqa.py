
import torch
from torch.nn import (
    Module,
    Sequential,
    Linear,
    ReLU,
    ModuleList,
)

from .message_passing import MessagePassing
from .encoder import Encoder
from .utils import layer_sizes_exp2
from config.config import RnaquanetConfig


class RnaQA(Module):
    def __init__(self, config: RnaquanetConfig):
        super().__init__()
        
        config = config.network
        self.config = config

        # Encoder
        self.encoder = Encoder(
            in_node_feats=config.encoder.in_node_feats,
            out_node_feats=config.encoder.out_node_feats,
            in_edge_feats=config.encoder.in_edge_feats,
            out_edge_feats=config.encoder.out_edge_feats,
        )

        # Message passing configuration
        # Configuration
        mp_edge_feats = layer_sizes_exp2(
            config.encoder.out_edge_feats, 
            config.message_passing.out_edge_feats, 
            config.message_passing.layers, 
            round_pow2=True
        )
        mp_node_feats = layer_sizes_exp2(
            config.encoder.out_node_feats, 
            config.message_passing.out_node_feats,
            config.message_passing.layers, 
            round_pow2=True
        )
        mp_global_feats = layer_sizes_exp2(
            config.message_passing.in_global_feats,
            config.message_passing.out_global_feats,
            config.message_passing.layers,
            round_pow2=True,
        )
        mp_sizes = zip(mp_edge_feats, mp_node_feats, [0] + mp_global_feats[1:])

        # Message passing
        self.message_passing = ModuleList()
        in_e, in_n, in_g = next(mp_sizes)
        for out_e, out_n, out_g in mp_sizes:
            mp = MessagePassing(
                in_edge_feats=in_e,
                in_node_feats=in_n,
                in_global_feats=in_g,
                out_edge_feats=out_e,
                out_node_feats=out_n,
                out_global_feats=out_g,
                dropout=config.message_passing.dropout,
                batch_norm=config.message_passing.batch_norm,
                scatter=config.message_passing.scatter,
            )
            self.message_passing.append(mp)
            in_e, in_n, in_g = out_e, out_n, out_g

        # Readout
        self.readout = Sequential(
            ReLU(),
            Linear(in_g, 128),
            ReLU(),
            Linear(128, 1)
        )

    def forward(
        self, x, edge_index, edge_attr, batch
    ):
        # Encoder
        x, edge_attr = self.encoder(x, edge_attr)


        # Message passing
        num_graphs = batch[-1].item() + 1
        u = torch.zeros(num_graphs, 0, dtype=torch.float, device=x.device)
        for mp in self.message_passing:
            x, edge_attr, edge_index, u, batch = mp(x, edge_attr, edge_index, u, batch)

        # Readout
        u = self.readout(u).view(-1)
        return u


