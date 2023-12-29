# Copyright 2023 The JAXampler Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import partial

import jax
from jax import Array, jit, lax
from jax import numpy as jnp
from jax.scipy.stats import uniform as jax_uniform
from jax.typing import ArrayLike

from ...utils import jx_cast
from .crvs import ContinuousRV


class Uniform(ContinuousRV):

    def __init__(self, low: ArrayLike = 0.0, high: ArrayLike = 1.0, name: str = None) -> None:
        self._low, self._high = jx_cast(low, high)
        self.check_params()
        super().__init__(name)

    def check_params(self) -> None:
        assert jnp.all(self._low < self._high), "All low must be less than high"

    @partial(jit, static_argnums=(0,))
    def logpdf(self, x: ArrayLike) -> ArrayLike:
        return jax_uniform.logpdf(x, loc=self._low, scale=self._high - self._low)

    @partial(jit, static_argnums=(0,))
    def pdf(self, x: ArrayLike) -> ArrayLike:
        return jax_uniform.pdf(x, loc=self._low, scale=self._high - self._low)

    @partial(jit, static_argnums=(0,))
    def logcdf(self, x: ArrayLike) -> ArrayLike:
        conditions = [x < self._low, (self._low <= x) & (x <= self._high), self._high < x]
        choice = [
            -jnp.inf,
            lax.log(x - self._low) - lax.log(self._high - self._low),
            jnp.log(1.0),
        ]
        return jnp.select(conditions, choice)

    def rvs(self, N: int = 1, key: Array = None) -> Array:
        if key is None:
            key = self.get_key(key)
        shape = (N,) + (self._low.shape or (1,))
        return jax.random.uniform(key, minval=self._low, maxval=self._high, shape=shape)

    def __repr__(self) -> str:
        string = f"Uniform(low={self._low}, high={self._high}"
        if self._name is not None:
            string += f", name={self._name}"
        string += ")"
        return string
