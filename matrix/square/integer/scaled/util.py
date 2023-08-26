from math import lcm, gcd


class FractionScaledMatrixUtilMixin:
    def _gcd_nonzero_elements(self, *args):
        nonzero_elements = [num for num in args if num != 0]
        if len(nonzero_elements) == 0:
            return 1
        result = abs(nonzero_elements[0])
        if result == 1:
            return 1
        for num in nonzero_elements[1:]:
            if num == 1:
                return 1
            result = gcd(result, num)
        return result

    def _lcm_nonzero_elements(self, *args):
        nonzero_elements = [num for num in args if num > 1]
        if len(nonzero_elements) == 0:
            return 1
        result = nonzero_elements[0]
        for num in nonzero_elements[1:]:
            result = lcm(result, num)
        return result

    def _calculate_element_quotients(self, divisor, *args):
        quotients = [(dividend // divisor, 1) if dividend %
                     divisor == 0 else (dividend, divisor) for dividend in args]
        denominator_lcm = 1
        for quotient in quotients:
            denominator = quotient[1]
            denominator_lcm = lcm(denominator_lcm, denominator)
        scaled_quotients = [numerator * denominator_lcm // denominator
                            for (numerator, denominator) in quotients]
        return denominator_lcm, scaled_quotients
