import os
from rnaquanet.network.rnaquanet import get_empty_model
import torch
from torch_geometric.data import Data
from rnaquanet.data.preprocessing.preprocess_utils import process_single_structure
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from utils.parser import RnaquanetParser
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    parser = RnaquanetParser(description="Eval network")
    parser.add_argument('--input', '-i', metavar='file', default='file.pdb', help='Path to PDB file')
    config = parser.get_config()
    args = parser.parse_args()

    config.name = 'tmp'

    model = get_empty_model('ares')
    model.load_state_dict(torch.load(f'/app/models/ares.pt', map_location=torch.device('cpu')))

    _, data = process_single_structure([args.input, config, None])
    model.eval()
    for sample in DataLoader([data], batch_size=1):
        print(model(torch.nan_to_num(sample.x, nan=1000), sample.edge_index, sample.edge_attr, sample.batch).item())


