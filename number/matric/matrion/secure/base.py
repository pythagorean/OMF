from number.matric.matrion.base import Matrion

from number.matric.matrion.secure.__init__ import SecureMatrionInitMixin
from number.matric.matrion.secure.ops import SecureMatrionOpsMixin


class SecureMatrion(SecureMatrionInitMixin,
                    SecureMatrionOpsMixin,
                    Matrion):
    pass
