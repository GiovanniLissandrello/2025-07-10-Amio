from dataclasses import dataclass
from model.product import Product


@dataclass
class Arco:
    u : Product
    v : Product
    peso : int
