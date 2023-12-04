from rnaquanet.data.preprocessing.preprocess_utils import process_structures
from utils.parser import RnaquanetParser

if __name__ == '__main__':
    parser = RnaquanetParser(description="Preprocess data")
    config = parser.get_config()

    process_structures(config)

