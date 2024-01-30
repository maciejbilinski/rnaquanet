import os
import shutil

from rnaquanet.data.preprocessing.extract.node.basepairs_features import extract_basepairs
from rnaquanet.data.preprocessing.extract.node.files_features import get_features_from_file
from rnaquanet.data.preprocessing.extract.node.nucleotides_features import extract_nucleotides
from rnaquanet.data.preprocessing.extract_features import extract_features
from rnaquanet.data.preprocessing.pdb_filter import filter_file
from rnaquanet.data.preprocessing.preprocess_utils import process_single_structure
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig

if __name__ == '__main__':
    config = RnaquanetConfig(os.path.join(os.path.dirname(__file__), 'config_test.yml'))

    filename = '157d_S_000004_minimize_001.pdb'
    file = os.path.join(config.data.path, config.name, 'archive', 'train', filename)

    if not os.path.isfile(file):
        raise Exception('Please download dataset first `python cli/download_raw_data.py -c tests/config_test.yml` or run download_raw_data test')
    
    preprocessing_path = os.path.join(config.data.path, config.name, 'preprocessing')
    if os.path.exists(preprocessing_path):
        shutil.rmtree(preprocessing_path)

    filtered_file_path = filter_file(config, file)
    assert os.path.isfile(filtered_file_path)

    features_file_path = extract_features(config, filtered_file_path)
    assert len(os.listdir(features_file_path)) == 8

    sequence_feature = extract_nucleotides(filtered_file_path)
    assert sequence_feature.shape[1] == 4
    assert sequence_feature.sum().sum() == sequence_feature.shape[0]
          
    basepairs_feature = extract_basepairs(filtered_file_path, distinguish = False)
    assert basepairs_feature.shape[1] == 5
    assert basepairs_feature.sum().sum() == sequence_feature.shape[0]

    basepairs_feature = extract_basepairs(filtered_file_path, distinguish = True)
    assert basepairs_feature.shape[1] == 9
    assert basepairs_feature.sum().sum() == sequence_feature.shape[0]

    bon_features = get_features_from_file(features_file_path, 'bon')
    assert bon_features.shape[1] == 32
    ang_features = get_features_from_file(features_file_path, 'ang')
    assert ang_features.shape[1] == 8
    atr_features = get_features_from_file(features_file_path, 'atr')
    assert atr_features.shape[1] == 47

    shutil.rmtree(os.path.join(config.data.path, config.name, 'preprocessing'))
    
    structure_name, data = process_single_structure([file, config, None])
    assert structure_name == filename.split('.')[0]
    assert str(data) == 'Data(x=[24, 99], edge_index=[2, 198], edge_attr=[198, 2])'

    shutil.rmtree(os.path.join(config.data.path, config.name, 'preprocessing'))

    structure_name, data = process_single_structure([file, config, 12])
    assert structure_name == filename.split('.')[0]
    assert str(data) == 'Data(x=[24, 99], edge_index=[2, 198], edge_attr=[198, 2], y=12)'