from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Tuple
from shapely import Point
from numpy.random import random_sample
from math import ceil, pi, sqrt
import numpy as np


@dataclass(slots=True, order=True)
class Candidate:
    fitness: float | None
    value: Point


@dataclass(kw_only=True)
class GeneticPoints:
    fit_func: Callable[[Point], float]

    min_mutation_distance: float = .01
    max_mutation_distance: float = .5

    mate_maximum: int = 0
    mate_border: int = int(ceil((sqrt(8*mate_maximum+1)-1)/2))

    mutation_maximum: int = 39

    inmutate_maximum: int = 10

    minimize: bool = False

    __rs = np.random.RandomState()

    __min_fitness_total = float('inf')
    __max_fitness_total = float('-inf')

    generation = 0

    def mutate(
            self,
            candidates: Iterable[Candidate],
            rs: np.random.RandomState = __rs) -> List[Candidate]:
        self.calculate_fitness(candidates)
        xs = np.fromiter((c.value.x for c in candidates), dtype=float)
        ys = np.fromiter((c.value.y for c in candidates), dtype=float)
        fs = np.fromiter((c.fitness for c in candidates), dtype=float)

        m_distance = np.interp(
            fs,
            (self.__min_fitness_total, self.__max_fitness_total),
            (self.min_mutation_distance if self.minimize else self.max_mutation_distance,
             self.max_mutation_distance if self.minimize else self.min_mutation_distance)
        )

        count = len(xs)

        ra = rs.random_sample(count)*(2*pi)

        x_offs = np.sin(ra)*m_distance
        y_offs = np.cos(ra)*m_distance

        moved_xs = xs+x_offs
        moved_ys = ys+y_offs

        xs_r, x_int = np.modf(moved_xs)
        ys_r, y_int = np.modf(moved_ys)

        xs = xs_r*((x_int >= 0.0).astype(float)
                   )+(1.0-xs_r)*((moved_xs < 0.0).astype(float))
        ys = ys_r*((y_int >= 0.0).astype(float)
                   )+(1.0-ys_r)*((moved_ys < 0.0).astype(float))

        return [Candidate(None, Point(x, y)) for x, y in zip(xs, ys)]

    def mate(self,
             candidates_a: List[Candidate],
             candidates_b: List[Candidate]) -> List[Candidate]:
        count = min(len(candidates_a), len(candidates_b))

        xs_a = np.fromiter(
            (c.value.x for c in candidates_a[: count]),
            dtype=float)
        xs_b = np.fromiter(
            (c.value.x for c in candidates_b[: count]),
            dtype=float)

        ys_a = np.fromiter(
            (c.value.y for c in candidates_a[: count]),
            dtype=float)
        ys_b = np.fromiter(
            (c.value.y for c in candidates_b[: count]),
            dtype=float)

        xs = (xs_a+xs_b)/2.0
        ys = (ys_a+ys_b)/2.0

        return [Candidate(None, Point(x, y)) for x, y in zip(xs, ys)][:self.mate_maximum]

    def calculate_fitness(
            self,
            candidates: Iterable[Candidate]) -> None:
        for c in candidates:
            if c.fitness is None:
                c.fitness = self.fit_func(c.value)
            self.__min_fitness_total = min(self.__min_fitness_total, c.fitness)
            self.__max_fitness_total = max(self.__max_fitness_total, c.fitness)

    def mate_selection(self, candidates: List[Candidate]) -> Tuple[List[Candidate],
                                                                   List[Candidate]]:
        self.calculate_fitness(candidates)

        candidates.sort(reverse=not (self.minimize), key=lambda x: x.fitness)

        pairs: List[Tuple[int, int]] = []

        limit = min(self.mate_border+1, len(candidates))
        for a_i, _ in enumerate(candidates[:limit]):
            for b_i, _ in enumerate(candidates[a_i+1:limit]):
                pairs.append((a_i, b_i))

        pairs.sort(key=lambda x: sum(x))

        return ([candidates[a] for a, _ in pairs], [candidates[b] for _, b in pairs])

    def mutate_selection(
            self,
            candidates: List[Candidate],
            rs: np.random.RandomState = __rs) -> List[Candidate]:
        return rs.choice(candidates, self.mutation_maximum)

    def next_gen(
            self,
            parents: List[Candidate] | None = None,
            rs: np.random.RandomState = __rs) -> List[Candidate]:
        try:
            self.__historical__ = self.__historical__
        except:
            self.__historical__ = {}

        if parents is None:
            parents = self.__historical__[self.generation]
        else:
            self.__historical__[self.generation] = parents

        mat = self.mate_selection(parents)
        mut = self.mutate_selection(parents, rs)

        limit = min(self.inmutate_maximum,len(parents))
        new_ones = parents[:limit]
        new_ones = new_ones+self.mate(*mat)
        new_ones = sorted(new_ones+self.mutate(mut), not (self.minimize))

        self.generation += 1

        self.__historical__[self.generation] = new_ones

        return new_ones

    @property
    def all_candidates(self) -> Dict[int, List[Candidate]]:
        return self.__historical__.copy()

    @property
    def last_candidates(self) -> List[Candidate]:
        return self.__historical__[self.generation].copy()
