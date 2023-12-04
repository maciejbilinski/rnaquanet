from typing import Iterable
from tqdm import tqdm
from .rnaquanet_config import RnaquanetConfig


class SafeTqdm(tqdm):
    def __init__(self, config: RnaquanetConfig, iterable: Iterable|None = None, total: float | None = None, unit: str = "it", unit_scale: bool | float = False):
        tqdm.__init__(self, iterable=iterable, total=total, unit=unit, unit_scale=unit_scale, disable=(not config.verbose))