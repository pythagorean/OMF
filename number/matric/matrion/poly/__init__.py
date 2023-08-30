from number.matric.matrion.factored.scaled.chained.base import ChainedMatrion
from number.matric.matrion.factored.scaled.base import VirtualScaledMatrion


class PolyMatrionInitMixin:
    def __init__(self, elements):
        if not isinstance((element := elements), list):
            elements = [VirtualScaledMatrion(element)]
        elif (len(elements) > 1 and not
              isinstance(elements[0], (VirtualScaledMatrion, ChainedMatrion))):
            elements = [VirtualScaledMatrion(elements)]
        super().__init__(sequence=elements)
