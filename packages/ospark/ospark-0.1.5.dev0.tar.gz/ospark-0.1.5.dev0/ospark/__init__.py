__version__ = "0.1.5.dev0"
__name__ = "ospark"
import logging
from ospark.nn.component.weight import Weight, WeightOperator
from ospark.nn.component.basic_module import ModelObject
from ospark.nn.layers import Layer, normalization, activation
from ospark.utility import weight_initializer
from ospark.nn.component import weight
from ospark.nn.model import Model
from ospark.nn.block import Block
from ospark.nn.cell import Cell


logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)