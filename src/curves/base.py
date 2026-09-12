"""Core analytic and polygonal curve containers.

The project deliberately keeps geometry objects light weight.  An analytic
component stores position and its first two parameter derivatives; a link is a
finite collection of components.  Parameter values are in the component's
native interval (``[0, period)`` for the built in closed curves).

No numerical value returned by this module is an interval certificate.  The
``metadata`` mapping is used to carry construction facts (for example the
torus winding numbers) without confusing them with a sampled topology test.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Iterator, Sequence

import numpy as np


VectorFunction = Callable[[float], Sequence[float]]


def _call_vector_function(function: Callable[[Any], Any], values: Any) -> np.ndarray:
    """Evaluate a 3-vector function for scalar or array parameters.

    Built in generators are vectorised, but this helper also supports a
    user-supplied scalar callable.  The returned shape is ``values.shape +
    (3,)`` (or ``(3,)`` for a scalar).
    """

    arr = np.asarray(values, dtype=float)
    if arr.ndim == 0:
        out = np.asarray(function(float(arr)), dtype=float)
        if out.shape != (3,):
            raise ValueError(f"vector function returned shape {out.shape}, expected (3,)")
        return out

    try:
        out = np.asarray(function(arr), dtype=float)
        if out.shape == arr.shape + (3,):
            return out
        if out.shape == (3,) + arr.shape:
            return np.moveaxis(out, 0, -1)
    except Exception:
        out = None

    flat = np.asarray([function(float(x)) for x in arr.ravel()], dtype=float)
    if flat.shape != (arr.size, 3):
        raise ValueError(f"vector function returned shape {flat.shape}, expected ({arr.size}, 3)")
    return flat.reshape(arr.shape + (3,))


@dataclass
class CurveComponent:
    """One parameterised curve component."""

    position_function: Callable[[Any], Any]
    derivative_function: Callable[[Any], Any]
    second_derivative_function: Callable[[Any], Any]
    period: float = 2.0 * np.pi
    closed: bool = True
    component: int = 0
    name: str = "component"
    metadata: dict[str, Any] = field(default_factory=dict)

    def evaluate(self, parameter: Any) -> np.ndarray:
        return _call_vector_function(self.position_function, parameter)

    position = evaluate

    def derivative(self, parameter: Any, order: int = 1) -> np.ndarray:
        if order == 0:
            return self.evaluate(parameter)
        if order == 1:
            return _call_vector_function(self.derivative_function, parameter)
        if order == 2:
            return _call_vector_function(self.second_derivative_function, parameter)
        raise ValueError("only derivatives of order 0, 1 and 2 are stored")

    def d1(self, parameter: Any) -> np.ndarray:
        return self.derivative(parameter, 1)

    def d2(self, parameter: Any) -> np.ndarray:
        return self.derivative(parameter, 2)

    def speed(self, parameter: Any) -> np.ndarray:
        return np.linalg.norm(self.d1(parameter), axis=-1)

    def length(self, *, atol: float = 1e-10, rtol: float = 1e-10) -> float:
        exact = self.metadata.get("exact_length")
        if exact is not None:
            return float(exact)
        try:
            from scipy.integrate import quad
        except Exception:  # pragma: no cover - scipy is part of the project env
            grid = np.linspace(0.0, self.period, 4097, endpoint=False)
            return float(np.trapz(self.speed(grid), grid))
        value, _ = quad(lambda t: float(self.speed(t)), 0.0, self.period, epsabs=atol, epsrel=rtol, limit=400)
        return float(value)

    def sample(self, count: int = 128, *, include_endpoint: bool = False) -> np.ndarray:
        if count < 2:
            raise ValueError("a sample needs at least two points")
        parameters = np.linspace(0.0, self.period, int(count), endpoint=include_endpoint)
        return np.asarray(self.evaluate(parameters), dtype=float)


class Curve:
    """A curve or finite link represented by analytic components."""

    def __init__(self, components: Iterable[CurveComponent], *, name: str = "curve", metadata: dict[str, Any] | None = None):
        values = tuple(components)
        if not values:
            raise ValueError("a curve must contain at least one component")
        self.components: tuple[CurveComponent, ...] = values
        self.name = name
        self.metadata: dict[str, Any] = dict(metadata or {})
        self.metadata.setdefault("component_count", len(values))

    def __iter__(self) -> Iterator[CurveComponent]:
        return iter(self.components)

    def __len__(self) -> int:
        return len(self.components)

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def closed(self) -> bool:
        return all(component.closed for component in self.components)

    def component(self, index: int = 0) -> CurveComponent:
        return self.components[int(index)]

    def evaluate(self, parameter: Any, component: int = 0) -> np.ndarray:
        return self.component(component).evaluate(parameter)

    position = evaluate

    def derivative(self, parameter: Any, order: int = 1, component: int = 0) -> np.ndarray:
        return self.component(component).derivative(parameter, order)

    def d1(self, parameter: Any, component: int = 0) -> np.ndarray:
        return self.component(component).d1(parameter)

    def d2(self, parameter: Any, component: int = 0) -> np.ndarray:
        return self.component(component).d2(parameter)

    def length(self, component: int | None = None) -> float:
        if component is None:
            return float(sum(item.length() for item in self.components))
        return self.component(component).length()

    @property
    def total_length(self) -> float:
        return self.length()

    def sample(self, count: int = 128, *, component: int | None = None, include_endpoint: bool = False):
        """Sample one component or all components.

        A single component is returned as an ``(count, 3)`` array.  Multiple
        components are returned as a list of arrays so components never get
        silently concatenated.
        """

        if component is not None:
            return self.component(component).sample(count, include_endpoint=include_endpoint)
        arrays = [item.sample(count, include_endpoint=include_endpoint) for item in self.components]
        return arrays[0] if len(arrays) == 1 else arrays

    def sample_components(self, count: int = 128, *, include_endpoint: bool = False) -> list[np.ndarray]:
        return [item.sample(count, include_endpoint=include_endpoint) for item in self.components]

    def with_metadata(self, **metadata: Any) -> "Curve":
        merged = dict(self.metadata)
        merged.update(metadata)
        return Curve(self.components, name=self.name, metadata=merged)


class Link(Curve):
    """Semantic alias for a multi-component ``Curve``.

    A one-component link is allowed because it is useful for a uniform API;
    callers should use ``component_count`` rather than the class name when
    deciding whether an object is a knot or link.
    """

    pass


def as_component(value: Any, *, count: int = 256, component: int = 0) -> CurveComponent:
    """Return an analytic component, sampling a supported curve if needed."""

    if isinstance(value, CurveComponent):
        return value
    if isinstance(value, Curve):
        return value.component(component)
    raise TypeError(f"expected CurveComponent or Curve, got {type(value).__name__}")


__all__ = ["Curve", "CurveComponent", "Link", "as_component"]
