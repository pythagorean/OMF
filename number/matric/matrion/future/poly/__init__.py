from number.matric.matrion.chained.base import ChainedMatrion
from number.matric.matrion.base import Matrion


class PolyMatrionInitMixin:
    def __init__(self, elements):
        if not isinstance((element := elements), list):
            elements = [Matrion(element)]
        elif (len(elements) > 1 and not
              isinstance(elements[0], (Matrion, ChainedMatrion))):
            elements = [Matrion(elements)]
        super().__init__(sequence=elements)
