import itertools
from fractions import Fraction
from functools import lru_cache
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


class DataMatrix:

    def __init__(self, observers: List[Dict[str, Optional[int]]]):
        self._observers = observers

    @property
    @lru_cache()
    def units(self) -> Tuple[str]:
        units = {unit for observer_results in self._observers for unit in observer_results.keys()}
        try:
            # In case units are integers try to retain normal numerical ordering
            return tuple(sorted(units, key=int))
        except ValueError:
            return tuple(sorted(units))

    @property
    @lru_cache()
    def values(self) -> Tuple[int]:
        max_result = 1
        for observer_results in self._observers:
            for result in observer_results.values():
                if result is not None and result > max_result:
                    max_result = result
        return tuple(range(1, max_result + 1))

    @property
    @lru_cache()
    def observer_names(self) -> Tuple[str]:
        return tuple(chr(65 + i) for i in range(len(self._observers)))

    @property
    def values_matrix(self) -> List[List[Optional[int]]]:
        return [
            [observer.get(unit) for unit in self.units]
            for observer in self._observers
        ]

    @property
    @lru_cache()
    def unit_pairs(self) -> Tuple[Tuple[str, str], ...]:
        return tuple(itertools.product(self.values, repeat=2))

    def get_observers_valuing_unit(self, unit) -> int:
        """
        Count number of observers valuing given unit, m_i
        """
        return sum(observer_result.get(unit) is not None for observer_result in self._observers)

    def get_c_k_pairs_in_unit(self, c: int, k: int, unit: str) -> Fraction:
        observers_valuing_unit = self.get_observers_valuing_unit(unit)
        if observers_valuing_unit < 2:
            return Fraction(0)

        c_k_pairs = sum(
            (observer_1.get(unit), observer_2.get(unit)) == (c, k)
            for observer_1, observer_2 in itertools.permutations(self._observers, 2)
        )
        return Fraction(c_k_pairs, observers_valuing_unit - 1)

    def get_observed_coincidence(self, c: int, k: int) -> Fraction:
        """
        Get coincidence for c-k pair o_ck.
        """
        return sum(self.get_c_k_pairs_in_unit(c, k, unit) for unit in self.units)

    def get_observed_coincidence_matrix(self) -> List[List[Fraction]]:
        return [
            [self.get_observed_coincidence(c, k) for k in self.values]
            for c in self.values
        ]

    def print_observed_coincidence_matrix(self):
        observed_coincidence_matrix = self.get_observed_coincidence_matrix()
        for row in observed_coincidence_matrix:
            for element in row:
                print(element, end='\t')
            print()

    @lru_cache()
    def get_number_of_values(self, value: int) -> Fraction:
        return sum(self.get_observed_coincidence(value, another_value) for another_value in self.values)

    @lru_cache()
    def get_total_number_of_values(self) -> int:
        return sum(map(self.get_number_of_values, self.values))

    def __str__(self):
        spacer_width = 80
        rows = [
            '\t'.join(map(str, ('', '|', *self.values, '|'))),
            '―' * spacer_width,
        ]
        observed_coincidence_matrix = self.get_observed_coincidence_matrix()
        for value, row in zip(self.values, observed_coincidence_matrix):
            rows.append('\t'.join(map(str, (value, '|', *row, '|', self.get_number_of_values(value)))))

        n = self.get_total_number_of_values()
        rows.extend([
            '―' * spacer_width,
            '\t'.join(map(str, ('', '|', *map(self.get_number_of_values, self.values), '|', n))),
        ])

        return '\n'.join(rows)

    @lru_cache()
    def compute_krippendorff_alpha(self) -> Fraction:
        def _n(value):
            return self.get_number_of_values(value)

        def _o(c, k):
            return self.get_observed_coincidence(c, k)

        n = self.get_total_number_of_values()

        return Fraction(
            (n - 1) * sum(_o(c, c) for c in self.values) - sum(_n(c) * (_n(c) - 1) for c in self.values),
            n * (n - 1) - sum(_n(c) * (_n(c) - 1) for c in self.values)
        )


if __name__ == '__main__':
    _observers = [
        # Observer A
        {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 1, '9': 2, '8': 1, '11': None, '10': None, '12': None},
        # Observer B
        {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 2, '9': 2, '8': 1, '11': None, '10': 5, '12': 3},
        # Observer C
        {'1': None, '3': 3, '2': 3, '5': 2, '4': 3, '7': 4, '6': 3, '9': 2, '8': 2, '11': 1, '10': 5, '12': None},
        # Observer D
        {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 4, '9': 2, '8': 1, '11': 1, '10': 5, '12': None},
    ]

    dm = DataMatrix(_observers)
    print(dm)
    alpha = dm.compute_krippendorff_alpha()
    print()
    print(f'alpha = {alpha}')
    print(f'alpha ~= {float(alpha)}')
