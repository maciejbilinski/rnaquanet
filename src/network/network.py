from typing import Tuple

import numpy as np
import torch
import torch_scatter
from torch_geometric.data import Batch, Data
from torch.nn import (
    Module,
    Sequential,
    Linear,
    ReLU,
    Sigmoid,
    Embedding,
    ModuleDict,
    ModuleList,
    Dropout,
    BatchNorm1d,
    Identity,
)


class GraphQA(Module):
    def __init__(self, conf):
        super().__init__()

        # Configuration
        mp_in_edge_feats = conf.encoder.out_edge_feats
        mp_in_node_feats = conf.encoder.out_node_feats

        mp_edge_feats = layer_sizes_exp2(
            mp_in_edge_feats, conf.mp.out_edge_feats, conf.mp.layers, round_pow2=True
        )
        mp_node_feats = layer_sizes_exp2(
            mp_in_node_feats, conf.mp.out_node_feats, conf.mp.layers, round_pow2=True
        )
        mp_global_feats = layer_sizes_exp2(
            conf.mp.in_global_feats,
            conf.mp.out_global_feats,
            conf.mp.layers,
            round_pow2=True,
        )
        mp_sizes = zip(mp_edge_feats, mp_node_feats, [0] + mp_global_feats[1:])

        # Encoder (dssp features on the nodes and geometric features on the edges)
        self.encoder = Encoder(
            out_edge_feats=conf.encoder.out_edge_feats,
            out_node_feats=conf.encoder.out_node_feats,
        )

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
                dropout=conf.mp.dropout,
                batch_norm=conf.mp.batch_norm,
                scatter=conf.mp.scatter,
            )
            self.message_passing.append(mp)
            in_e, in_n, in_g = out_e, out_n, out_g

        # Readout
        self.readout = Linear(in_g, 1)

    @staticmethod
    def prepare(graphs: Batch) -> Tuple[torch.Tensor, ...]:
        x = graphs.x
        edge_index = graphs.edge_index
        edge_attr = graphs.edge_attr
        batch = graphs.batch
        y = graphs.y

        return x, edge_index, edge_attr, batch, y

    def forward(
        self, x, edge_index, edge_attr, batch
    ):
        # Encoder (dssp features on the nodes and geometric features on the edges)
        x, edge_attr = self.encoder(x, edge_attr)

        # Message passing
        num_graphs = batch[-1].item() + 1
        u = torch.empty(num_graphs, 0, dtype=torch.float, device=x.device)
        for mp in self.message_passing:
            x, edge_attr, edge_index, u, batch = mp(x, edge_attr, edge_index, u, batch)

        # Readout
        u = self.readout(u).view(-1)
        return u

class Encoder(Module):
    def __init__(self, out_edge_feats, out_node_feats):
        super().__init__()
        self.node_encoder = Sequential(
            Linear(96, out_node_feats // 2),
            ReLU(),
            Linear(out_node_feats // 2, out_node_feats),
            ReLU(),
        )
        self.edge_encoder = Sequential(
            Linear(1, out_edge_feats // 2),
            ReLU(),
            Linear(out_edge_feats // 2, out_edge_feats),
            ReLU(),
        )

    def forward(self, x, edge_attr):
        x = self.node_encoder(x)
        edge_attr = self.edge_encoder(edge_attr)
        return x, edge_attr


class MessagePassing(Module):
    def __init__(
        self,
        in_edge_feats: int,
        in_node_feats: int,
        in_global_feats: int,
        out_edge_feats: int,
        out_node_feats: int,
        out_global_feats: int,
        batch_norm: bool,
        dropout: float,
        scatter: str,
    ):
        super().__init__()
        in_feats = in_node_feats + in_edge_feats + in_global_feats
        self.edge_fn = Sequential(
            Linear(in_feats, out_edge_feats),
            Dropout(p=dropout) if dropout > 0 else Identity(),
            BatchNorm1d(out_edge_feats) if batch_norm else Identity(),
            ReLU(),
        )
        in_feats = in_node_feats + out_edge_feats + in_global_feats
        self.node_fn = Sequential(
            Linear(in_feats, out_node_feats),
            Dropout(p=dropout) if dropout > 0 else Identity(),
            BatchNorm1d(out_node_feats) if batch_norm else Identity(),
            ReLU(),
        )
        in_feats = out_node_feats + out_edge_feats + in_global_feats
        self.global_fn = Sequential(
            Linear(in_feats, out_global_feats),
            Dropout(p=dropout) if dropout > 0 else Identity(),
            BatchNorm1d(out_global_feats) if batch_norm else Identity(),
            ReLU(),
        )
        self.scatter = scatter

    def forward(self, x, edge_attr, edge_index, u, batch):
        x_src = x[edge_index[0]]
        u_src = u[batch[edge_index[0]]]
        edge_attr = torch.cat((x_src, edge_attr, u_src), dim=1)
        edge_attr = self.edge_fn(edge_attr)

        msg_to_node = torch_scatter.scatter(
            edge_attr, edge_index[1], dim=0, dim_size=x.shape[0], reduce=self.scatter
        )
        u_to_node = u[batch]
        x = torch.cat((x, msg_to_node, u_to_node), dim=1)
        x = self.node_fn(x)

        edge_global = torch_scatter.scatter(
            edge_attr,
            batch[edge_index[0]],
            dim=0,
            dim_size=u.shape[0],
            reduce=self.scatter,
        )
        x_global = torch_scatter.scatter(
            x, batch, dim=0, dim_size=u.shape[0], reduce=self.scatter
        )
        u = torch.cat((edge_global, x_global, u), dim=1)
        u = self.global_fn(u)

        return x, edge_attr, edge_index, u, batch

def round_to_pow2(value):
    return np.exp2(np.round(np.log2(value))).astype(int)


def layer_sizes_linear(in_feats, out_feats, layers, round_pow2=False):
    sizes = np.linspace(in_feats, out_feats, layers + 1).round().astype(np.int32)
    if round_pow2:
        sizes[1:-1] = round_to_pow2(sizes[1:-1])
    return sizes.tolist()


def layer_sizes_exp2(in_feats, out_feats, layers, round_pow2=False):
    sizes = (
        np.logspace(np.log2(in_feats), np.log2(out_feats), layers + 1, base=2)
        .round()
        .astype(np.int32)
    )
    if round_pow2:
        sizes[1:-1] = round_to_pow2(sizes[1:-1])
    return sizes.tolist()
    