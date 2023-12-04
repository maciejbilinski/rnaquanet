from .rnaquanet_config import RnaquanetConfig


def safe_print(config: RnaquanetConfig, value: object, sep: str | None = " ", end: str | None = "\n"):
    if config.verbose:
        print(value, sep=sep, end=end)