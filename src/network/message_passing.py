from torch.nn import (
    Module,
    Sequential,
    Linear,
    ReLU,
    Dropout,
    BatchNorm1d,
    Identity,
)
import torch_scatter
import torch

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