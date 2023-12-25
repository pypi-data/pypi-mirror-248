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
from jax.typing import ArrayLike

from ..rvs import GenericRV


class ContinuousRV(GenericRV):

    def __init__(self, name: str = None) -> None:
        super().__init__(name)

    @partial(jit, static_argnums=(0,))
    def Z(self) -> ArrayLike:
        return jnp.exp(self._logZ)

    def logpdf(self, *x: ArrayLike) -> ArrayLike:
        raise NotImplementedError

    @partial(jit, static_argnums=(0,))
    def pdf(self, *x: ArrayLike) -> ArrayLike:
        return jnp.exp(self.logpdf(*x))

    def __str__(self) -> str:
        return super().__str__()
