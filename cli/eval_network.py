import os
import torch
import pytorch_lightning as pl
import matplotlib.pyplot as plt
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from rnaquanet.network.h5_graph_dataset import H5GraphDataset
from utils.parser import RnaquanetParser
from time import time_ns
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    parser = RnaquanetParser(description="Eval network")
    parser.add_argument('--model', '-m', metavar='file', default='model.cpkt', help='Path to GraphRegressionNetwork model')
    config = parser.get_config()
    args = parser.parse_args()

    torch.set_float32_matmul_precision('high')
    
    config.network.batch_size = 1
    with H5GraphDataset(os.path.join('data', config.name, 'test.h5')) as data:
        model = GraphRegressionNetwork.load_from_checkpoint(os.path.join(os.getcwd(), args.model), config=config)
        trainer = pl.Trainer()
        trainer.test(model, dataloaders=DataLoader(data, batch_size=config.network.batch_size, shuffle=config.network.shuffle_test, num_workers=config.network.num_workers), )

        plt.hist(model.test_step_outputs)
        plt.title('Histogram of Test Losses')
        plt.xlabel('Loss')
        plt.ylabel('Frequency')
        plt.savefig(f'/app/analysis/eval_{config.name}_{time_ns()}.png')


