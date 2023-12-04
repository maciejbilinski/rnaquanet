import os
from rnaquanet.data.preprocessing.preprocess_utils import process_single_structure
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from utils.parser import RnaquanetParser
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    parser = RnaquanetParser(description="Eval network")
    parser.add_argument('--model', '-m', metavar='file', default='model.cpkt', help='Path to GraphRegressionNetwork model')
    parser.add_argument('--input', '-i', metavar='file', default='file.pdb', help='Path to PDB file')
    config = parser.get_config()
    args = parser.parse_args()

    config.name = 'tmp'
    model = GraphRegressionNetwork.load_from_checkpoint(os.path.join(os.getcwd(), args.model), config=config).cpu()
    _, data = process_single_structure([args.input, config, None])
    model.eval()
    for sample in DataLoader([data], batch_size=1):
        print(model(sample.x, sample.edge_index, sample.edge_attr, sample.batch).item())


