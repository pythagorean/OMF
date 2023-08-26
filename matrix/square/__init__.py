from pydantic import BaseModel


class SquareMatrixInitMixin(BaseModel):
    def __init__(self, matrix, **kwargs):
        size, validated_matrix = self.validate_matrix(matrix)
        super().__init__(size=size, matrix=validated_matrix, **kwargs)

    @staticmethod
    def validate_scalar(scalar):
        if not scalar:
            raise ValueError("Square matrix may not be empty")
        return 1, [[scalar]]

    @staticmethod
    def validate_flat_list(flat_list):
        flat_size = len(flat_list)
        size = int(flat_size ** 0.5)
        if size * size != flat_size:
            raise ValueError(
                "Flat list does not form a square matrix")
        return size, [flat_list[i:i + size] for i in range(0, flat_size, size)]

    @staticmethod
    def validate_square_matrix(matrix):
        size = len(matrix)
        if not all(isinstance(row, list) and len(row) == size for row in matrix):
            raise ValueError("Matrix must be square")
        return size, matrix

    def validate_matrix(self, data):
        if isinstance(data, list):
            if isinstance(data[0], list):
                return self.validate_square_matrix(data)
            return self.validate_flat_list(data)
        return self.validate_scalar(data)
