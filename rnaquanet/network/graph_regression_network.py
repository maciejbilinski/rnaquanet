from enum import Enum
import pytorch_lightning as pl
from torch.optim import Adam
from torch.nn import (
    BatchNorm1d,
    Identity,
    ModuleList
)
import torch.nn.functional as F
from torch_geometric.nn import (
    GATConv,
    TransformerConv,
    GCNConv,
    global_mean_pool
)
from torch.optim.lr_scheduler import StepLR
import numpy as np

from rnaquanet.utils.rnaquanet_config import RnaquanetConfig

class GRNLayerType(Enum):
    GCN = 1,
    GAT = 2,
    GCN_GAT = 3,
    GAT_TRANSFORMER = 4

class GraphRegressionNetwork(pl.LightningModule):
    def _get_layers_sizes(self, N, A, B):
        first_half_size = N // 2
        first_half = np.linspace(A, B, first_half_size, endpoint=True, dtype=int)

        second_half_size = N - first_half_size
        second_half = np.linspace(B, 1, second_half_size, endpoint=True, dtype=int)

        result_array = np.concatenate((first_half, second_half))

        return result_array.tolist()

    def __init__(
        self, 
        config: RnaquanetConfig
    ):
        super(GraphRegressionNetwork, self).__init__()

        hidden_dim = config.network.hidden_dim
        layer_type = GRNLayerType(config.network.layer_type)
        num_of_layers = config.network.num_of_layers
        num_of_node_features = config.network.num_of_node_features
        batch_norm = config.network.batch_norm
        gat_dropout = config.network.gat_dropout
        num_of_heads = config.network.num_of_heads
        lr = config.network.lr
        weight_decay = config.network.weight_decay
        scheduler_step_size = config.network.scheduler_step_size
        scheduler_gamma = config.network.scheduler_gamma

        if num_of_layers < 1:
            raise ValueError('num_of_layers should be at least one')
        
        self.lr = lr
        self.weight_decay = weight_decay
        self.scheduler_step_size = scheduler_step_size
        self.scheduler_gamma = scheduler_gamma

        batch_norm_list: list[BatchNorm1d]|list[Identity] = []
        conv_list: list[GATConv]|list[GCNConv] = []
        sizes = self._get_layers_sizes(num_of_layers+1, num_of_node_features, hidden_dim)
        for i in range(num_of_layers):
            batch_norm_list.append(
                BatchNorm1d(sizes[i]) if batch_norm else Identity()
            )

            match layer_type:
                case GRNLayerType.GAT:
                    layer = GATConv(sizes[i], sizes[i+1], dropout=gat_dropout)
                case GRNLayerType.GCN_GAT:
                    if i % 2 == 0:
                        layer = GATConv(sizes[i], sizes[i+1], dropout=gat_dropout)
                    else:
                        layer = GCNConv(sizes[i], sizes[i+1]) 
                case GRNLayerType.GAT_TRANSFORMER:
                    layer = TransformerConv(sizes[i], sizes[i+1], heads=num_of_heads, dropout=gat_dropout) 
                
            conv_list.append(
                layer
            )

        self.batch_norm = ModuleList(batch_norm_list)
        self.conv = ModuleList(conv_list)
        self.test_step_outputs = []
        
    def forward(self, x, edge_index, edge_attr, batch):
        for batch_norm, conv in zip(self.batch_norm, self.conv):
            x = batch_norm(x)
            if isinstance(conv, GATConv):
                x = conv(x, edge_index, edge_attr)
            else:
                x = conv(x, edge_index)
            x = F.relu(x)
        
        x = global_mean_pool(x, batch) 
        
        return x
    
    def training_step(self, item, batch_idx):
        x = item.x
        edge_index = item.edge_index
        edge_attr = item.edge_attr
        batch = item.batch
        y = item.y.view(-1, 1)
        output = self(x, edge_index, edge_attr, batch)
        loss = F.mse_loss(output, y)
        self.log('train_loss', loss, on_epoch=True, prog_bar=True, batch_size=len(batch))
        return {
            # REQUIRED: It ie required for us to return "loss"
            "loss": loss,
            # optional for batch logging purposes
            "log": {"train_loss": loss},
        }
    
    def validation_step(self, item, batch_idx):
        x = item.x
        edge_index = item.edge_index
        edge_attr = item.edge_attr
        batch = item.batch
        y = item.y.view(-1, 1)
        output = self(x, edge_index, edge_attr, batch)
        loss = F.mse_loss(output, y)
        self.log('val_loss', loss, on_epoch=True, prog_bar=True, batch_size=len(batch))
        return {
            # REQUIRED: It ie required for us to return "loss"
            "loss": loss,
            # optional for batch logging purposes
            "log": {"val_loss": loss},
        }

    def test_step(self, item, batch_idx):
        x = item.x
        edge_index = item.edge_index
        edge_attr = item.edge_attr
        batch = item.batch
        y = item.y.view(-1, 1)
        output = self(x, edge_index, edge_attr, batch)
        loss = F.mse_loss(output, y)
        self.log('test_loss', loss, on_epoch=True, prog_bar=True, batch_size=len(batch))
        self.test_step_outputs.append(loss.item())
        return {
            # REQUIRED: It ie required for us to return "loss"
            "loss": loss,
            # optional for batch logging purposes
            "log": {"test_loss": loss},
        }
    
    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        scheduler = StepLR(optimizer, step_size=self.scheduler_step_size, gamma=self.scheduler_gamma)
        return [optimizer], [scheduler]
    

    def custom_histogram_adder(self):
        # iterating through all parameters
        for name,params in self.named_parameters():
            self.logger.experiment.add_histogram(name,params,self.current_epoch)