from torch.nn import (
    Module,
    Sequential,
    Linear,
    ReLU
)

class Encoder(Module):
    def __init__(self, in_edge_feats, out_edge_feats, in_node_feats, out_node_feats):
        super().__init__()
        self.node_encoder = Sequential(
            Linear(in_node_feats, out_node_feats // 2),
            ReLU(),
            Linear(out_node_feats // 2, out_node_feats),
            ReLU(),
        )
        self.edge_encoder = Sequential(
            Linear(in_edge_feats, out_edge_feats // 2),
            ReLU(),
            Linear(out_edge_feats // 2, out_edge_feats),
            ReLU(),
        )

    def forward(self, x, edge_attr):
        x = self.node_encoder(x)
        edge_attr = self.edge_encoder(edge_attr)
        return x, edge_attr