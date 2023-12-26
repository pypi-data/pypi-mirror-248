from ospark.data.processor.auto_click import AutoClick
from typing import *


class Test(metaclass=AutoClick):

    def __init__(self,
                 a: int=8,
                 b: Tuple[float]=(1.2, 4.5, 3.1),
                 c: Dict[str, List[List[int]]]={"a": [[1,2,3], [4,5,6]]}):
        pass

    def main_process(self):
        print(self._a)
        print(self._b)
        print(self._c["a"])

if __name__ == "__main__":
    Test()