from rnaquanet.data.download_utils import download_archive, extract_archive

from utils.parser import RnaquanetParser
if __name__ == '__main__':
    parser = RnaquanetParser(description="Download raw data")
    config = parser.get_config()

    download_archive(config)
    extract_archive(config)