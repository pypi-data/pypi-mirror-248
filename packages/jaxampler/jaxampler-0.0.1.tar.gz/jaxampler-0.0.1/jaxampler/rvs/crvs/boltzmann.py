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

from jax import jit
from jax import numpy as jnp
from jax.scipy.special import erf
from jax.typing import ArrayLike

from .crvs import ContinuousRV


class Boltzmann(ContinuousRV):

    def __init__(self, a: ArrayLike, name: str = None) -> None:
        self._a = a
        self.check_params()
        super().__init__(name)

    def check_params(self) -> None:
        assert jnp.all(self._a > 0.0), "a must be positive"

    @partial(jit, static_argnums=(0,))
    def logpdf(self, x: ArrayLike) -> ArrayLike:
        logpdf_val = 2 * jnp.log(x) - 0.5 * jnp.power(x / self._a, 2)
        logpdf_val -= 0.5 * jnp.log(jnp.pi / 2) + 3 * jnp.log(self._a)
        logpdf_val = jnp.where(x > 0.0, logpdf_val, jnp.nan)
        return logpdf_val

    @partial(jit, static_argnums=(0,))
    def cdf(self, x: ArrayLike) -> ArrayLike:
        cdf_val = jnp.log(x) - 0.5 * jnp.power(x / self._a, 2)
        cdf_val -= 0.5 * jnp.log(jnp.pi / 2) + jnp.log(self._a)
        cdf_val = jnp.exp(cdf_val)
        cdf_val = erf(x / (jnp.sqrt(2) * self._a)) - cdf_val
        return cdf_val

    def __repr__(self) -> str:
        string = f"Boltzmann(a={self._a}"
        if self._name is not None:
            string += f", name={self._name}"
        string += ")"
        return string
