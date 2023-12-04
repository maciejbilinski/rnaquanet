import argparse
import os
from typing import Any, Sequence

from rnaquanet.utils.rnaquanet_config import RnaquanetConfig


class RnaquanetParser(argparse.ArgumentParser):
    def __init__(
        self,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None
    ):
        argparse.ArgumentParser.__init__(self, prog=prog, usage=usage, description=description)
        self.add_argument('--config', '-c', metavar='file', default='config.yml', help='Path to the configuration file')

        self.add_argument('--name', metavar='name', help='Name of the dataset')
        self.add_argument('--tools-path', metavar='path', help='Path to the folder with external tools used in the pipeline')
        self.add_argument('--verbose', default=None, action=argparse.BooleanOptionalAction, help='Enable verbose mode')

        self.add_argument('--data-path', metavar='path', help='Path to the folder where data will be saved')

        self.add_argument('--data-download-url', metavar='url', help='URL for downloading the dataset')
        self.add_argument('--data-download-archive-ext', metavar='extension', help='Type of archive: tar/tar.gz')
        self.add_argument('--data-download-train-folder', metavar='folder', help='Path to the folder inside the archive with the training set')
        self.add_argument('--data-download-val-folder', metavar='folder', help='Path to the folder inside the archive with the validation set')
        self.add_argument('--data-download-test-folder', metavar='folder', help='Path to the folder inside the archive with the test set')
        self.add_argument('--data-download-train-csv', metavar='file', help='Path to the CSV file containing RMSD values for each RNA structure in the training set')
        self.add_argument('--data-download-val-csv', metavar='file', help='Path to the CSV file containing RMSD values for each RNA structure in the validation set')
        self.add_argument('--data-download-test-csv', metavar='file', help='Path to the CSV file containing RMSD values for each RNA structure in the test set')
        self.add_argument('--data-download-csv-delimiter', metavar='delimiter', help='Separator used inside the CSV file (usually a comma)')
        self.add_argument('--data-download-csv-rmsd-column-name', metavar='name', help='Name of the column in the CSV file with RMSD values')
        self.add_argument('--data-download-csv-structure-column-name', metavar='name', help='Name of the column in the CSV file with the file names corresponding to RMSD')

        self.add_argument('--data-download-preprocessed-train-url', metavar='url', help='URL for downloading the preprocessed H5 file for the training set')
        self.add_argument('--data-download-preprocessed-val-url', metavar='url', help='URL for downloading the preprocessed H5 file for the validation set')
        self.add_argument('--data-download-preprocessed-test-url', metavar='url', help='URL for downloading the preprocessed H5 file for the test set')

        self.add_argument('--data-features-atom-for-distance-calculations', metavar='atom', help='Atom for distance calculations')
        self.add_argument('--data-features-max-euclidean-distance', metavar='distance', help='Maximum Euclidean distance')
        self.add_argument('--data-features-regenerate-features-when-exists', default=None, action=argparse.BooleanOptionalAction, help='Regenerate features when they already exist')

        self.add_argument('--network-model-output-path', metavar='path', help='Path to save the trained model')
        self.add_argument('--network-hidden-dim', metavar='dim', help='Hidden dimension of the network', type=int)
        self.add_argument('--network-layer-type', metavar='type', help='Type of layers in the network', choices=[0, 1, 2], type=int)
        self.add_argument('--network-num-of-layers', metavar='num', help='Number of layers in the network', type=int)
        self.add_argument('--network-num-of-node-features', metavar='num', help='Number of node features', type=int)
        self.add_argument('--network-batch-norm', default=None, action=argparse.BooleanOptionalAction, help='Enable batch normalization')
        self.add_argument('--network-gat-dropout', metavar='dropout', help='GAT dropout rate', type=float)
        self.add_argument('--network-lr', metavar='rate', help='Learning rate', type=float)
        self.add_argument('--network-weight-decay', metavar='decay', help='Weight decay', type=float)
        self.add_argument('--network-scheduler-step-size', metavar='size', help='Scheduler step size', type=int)
        self.add_argument('--network-scheduler-gamma', metavar='gamma', help='Scheduler gamma', type=float)
        self.add_argument('--network-batch-size', metavar='size', help='Batch size for training', type=int)
        self.add_argument('--network-num-workers', metavar='num', help='Number of workers for data loading', type=int)
        self.add_argument('--network-shuffle-train', default=None, action=argparse.BooleanOptionalAction, help='Shuffle the training set')
        self.add_argument('--network-shuffle-val', default=None, action=argparse.BooleanOptionalAction, help='Shuffle the validation set')
        self.add_argument('--network-shuffle-test', default=None, action=argparse.BooleanOptionalAction, help='Shuffle the test set')
        self.add_argument('--network-max-epochs', metavar='epochs', help='Maximum number of training epochs', type=int)
    
    def parse_args(
        self,
        args: Sequence[str] | None = None,
        namespace: None = None
    ) -> argparse.Namespace: 
        args = argparse.ArgumentParser.parse_args(self, args=args, namespace=namespace)
        if args.data_download_url is not None:
            if args.data_download_url.lower() == 'false':
                args.data_download_url = False
        return args
        
    def get_config(self):
        args = self.parse_args()
        return RnaquanetConfig(os.path.join(os.getcwd(), args.config), override={
            'name': args.name,
            'tools_path': args.tools_path,
            'verbose': args.verbose,
            'data': {
                'path': args.data_path,
                'download': {
                    'url': args.data_download_url,
                    'archive_ext': args.data_download_archive_ext,
                    'train_folder': args.data_download_train_folder,
                    'val_folder': args.data_download_val_folder,
                    'test_folder': args.data_download_test_folder,
                    'train_csv': args.data_download_train_csv,
                    'val_csv': args.data_download_val_csv,
                    'test_csv': args.data_download_test_csv,
                    'csv_delimiter': args.data_download_csv_delimiter,
                    'csv_rmsd_column_name': args.data_download_csv_rmsd_column_name,
                    'csv_structure_column_name': args.data_download_csv_structure_column_name
                },
                'download_preprocessed': {
                    'train_url': args.data_download_preprocessed_train_url,
                    'val_url': args.data_download_preprocessed_val_url,
                    'test_url': args.data_download_preprocessed_test_url
                },
                'features': {
                    'atom_for_distance_calculations': args.data_features_atom_for_distance_calculations,
                    'max_euclidean_distance': args.data_features_max_euclidean_distance,
                    'regenerate_features_when_exists': args.data_features_regenerate_features_when_exists
                }
            },
            'network': {
                'model_output_path': args.network_model_output_path,
                'hidden_dim': args.network_hidden_dim,
                'layer_type': args.network_layer_type,
                'num_of_layers': args.network_num_of_layers,
                'num_of_node_features': args.network_num_of_node_features,
                'batch_norm': args.network_batch_norm,
                'gat_dropout': args.network_gat_dropout,
                'lr': args.network_lr,
                'weight_decay': args.network_weight_decay,
                'scheduler_step_size': args.network_scheduler_step_size,
                'scheduler_gamma': args.network_scheduler_gamma,
                'batch_size': args.network_batch_size,
                'num_workers': args.network_num_workers,
                'shuffle_train': args.network_shuffle_train,
                'shuffle_val': args.network_shuffle_val,
                'shuffle_test': args.network_shuffle_test,
                'max_epochs': args.network_max_epochs
            }
        })