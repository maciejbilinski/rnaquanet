from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.data.download_utils import download_preprocessed

from utils.parser import RnaquanetParser
if __name__ == '__main__':
    parser = RnaquanetParser(description="Download preprocessed data")
    download_preprocessed(parser.get_config())
