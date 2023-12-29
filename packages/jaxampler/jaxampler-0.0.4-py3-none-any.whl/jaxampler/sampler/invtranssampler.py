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

import jax
from jax import Array

from ..rvs import ContinuousRV
from .sampler import Sampler


class InverseTransformSampler(Sampler):
    """InverseTransformSampler is a sampler that uses the inverse transform
    method to sample from a random variable."""

    def __init__(self) -> None:
        """Initializes an InverseTransformSampler object."""
        super().__init__()

    def sample(self, rv: ContinuousRV, N: int = 1, key: Array = None) -> Array:
        """Samples from the given random variable using the inverse transform method.

        It runs the inverse transform algorithm and returns the samples.

        Parameters
        ----------
        rv : ContinuousRV
            The random variable to sample from.
        N : int, optional
            Number of samples, by default 1
        key : Array, optional
            The key to use for sampling, by default None

        Returns
        -------
        Array
            The samples.
        """
        self.check_rv(rv)

        if key is None:
            key = self.get_key(key)

        U = jax.random.uniform(key, shape=(N, 1))
        samples = rv.ppf(U)

        return samples
