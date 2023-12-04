import os
import torch
import pytorch_lightning as pl
import matplotlib.pyplot as plt
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from rnaquanet.network.grn_data_module import GRNDataModule
from utils.parser import RnaquanetParser
from time import time_ns

if __name__ == '__main__':
    parser = RnaquanetParser(description="Eval network")
    parser.add_argument('--model', '-m', metavar='file', default='model.cpkt', help='Path to GraphRegressionNetwork model')
    config = parser.get_config()
    args = parser.parse_args()

    torch.set_float32_matmul_precision('high')
    
    config.network.batch_size = 1
    data = GRNDataModule(config)
    data.prepare_data()

    model = GraphRegressionNetwork.load_from_checkpoint(os.path.join(os.getcwd(), args.model), config=config)
    trainer = pl.Trainer()
    trainer.test(model, datamodule=data)

    plt.hist(model.test_step_outputs)
    plt.title('Histogram of Test Losses')
    plt.xlabel('Loss')
    plt.ylabel('Frequency')
    plt.savefig(f'/app/analysis/eval_{config.name}_{time_ns()}.png')


