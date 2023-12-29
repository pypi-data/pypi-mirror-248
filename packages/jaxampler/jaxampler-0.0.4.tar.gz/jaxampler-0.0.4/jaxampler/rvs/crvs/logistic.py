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
from jax import Array, jit
from jax import numpy as jnp
from jax.scipy.special import logit
from jax.scipy.stats import logistic as jax_logistic
from jax.typing import ArrayLike

from ...utils import jx_cast
from .crvs import ContinuousRV


class Logistic(ContinuousRV):

    def __init__(self, mu: ArrayLike = 0.0, scale: ArrayLike = 1.0, name: str = None) -> None:
        self._scale, = jx_cast(scale)
        self.check_params()
        self._mu = mu
        super().__init__(name)

    def check_params(self) -> None:
        assert jnp.all(self._scale > 0.0), "scale must be positive"

    @partial(jit, static_argnums=(0,))
    def logpdf(self, x: ArrayLike) -> ArrayLike:
        return jax_logistic.logpdf(x, self._mu, self._scale)

    @partial(jit, static_argnums=(0,))
    def pdf(self, x: ArrayLike) -> ArrayLike:
        return jax_logistic.pdf(x, self._mu, self._scale)

    @partial(jit, static_argnums=(0,))
    def cdf(self, x: ArrayLike) -> ArrayLike:
        return jax_logistic.cdf(x, self._mu, self._scale)

    @partial(jit, static_argnums=(0,))
    def ppf(self, x: ArrayLike) -> ArrayLike:
        return self._mu + self._scale * logit(x)

    def rvs(self, N: int = 1, key: Array = None) -> Array:
        if key is None:
            key = self.get_key(key)
        shape = (N,) + (self._scale.shape or (1,))
        return jax.random.logistic(key, shape=shape) * self._scale + self._mu

    def __repr__(self) -> str:
        string = f"Logistic(mu={self._mu}, scale={self._scale}"
        if self._name is not None:
            string += f", name={self._name}"
        string += ")"
        return string
