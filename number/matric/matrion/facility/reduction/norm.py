class ReducedMatrionNormMixin:
    def _normalize(self):
        # Check if already reduced
        if self.reduced:
            return
        super()._normalize()
        self.reduced = True
        # Skip further normalization for 1x1 matrices
        if self.value.size == 1:
            return
        performed = []
        # Iterate through all available reduction transforms
        for reduction in self.reductions:
            result = reduction.normalize(self)
            # Skip if no reduction is performed
            if result is None:
                continue
            # Validate that the result is a tuple
            if not isinstance(result, tuple):
                raise ValueError(
                    f"Reduction '{reduction.__name__}' returned non-tuple")
            should_perform = result[0]
            # Skip if the reduction should not be performed
            if not should_perform:
                continue
             # Validate that the result tuple contains a factor
            if len(result) < 2:
                raise ValueError(
                    f"Reduction '{reduction.__name__}' lacks factor")
            factor = result[1]
            # Handle case where no extra data is provided
            if len(result) == 2:
                performed.append((reduction, factor, {}))
                continue
            extra = result[2]
            # Validate that extra data is a dictionary
            if not isinstance(extra, dict):
                raise ValueError(
                    f"Reduction '{reduction.__name__}' extra is non-dict")
            # Validate that the result tuple doesn't contain too many elements
            if len(result) > 3:
                raise ValueError(
                    f"Reduction '{reduction.__name__}' returned too many values")
            performed.append((reduction, factor, extra))
        # Store the performed reductions
        self.performed_reductions.extend(reversed(performed))

    def _denormalized(self):
        from number.matric.matrion.base import Matrion
        # If the matrix is not reduced, return the original value
        if not self.reduced:
            return self.value
        matrion = self
        # Iterate through all performed reductions to denormalize
        for performed in self.performed_reductions:
            reduction, factor, extra = performed
            # Call the denormalized method with the appropriate number of parameters
            if not extra:
                result = reduction.denormalized(matrion, factor)
            else:
                result = reduction.denormalized(matrion, factor, extra)
            # Create a new Matrion instance with the denormalized result
            matrion = Matrion(result, normalize=False)
        return matrion.value
