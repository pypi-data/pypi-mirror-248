import jax.numpy as jnp
from jax import jit
import numpy as np

from typing import Tuple, Union, Optional
from numpy.typing import NDArray
from ._quaternion import random_quaternion, apply_quaternion, Q

class T() :
    def __init__(self, translation: Optional[NDArray], quaternion: Optional[Q]) :
        self.translation = translation
        self.quaternion = quaternion

    def __call__(self, coords, center) :
        return __do_transform(coords, center, self.translation, self.quaternion)

class RandomTransform() :
    def __init__(
        self,
        random_translation: float = 0.0,
        random_rotation: bool = False,
    ) :
        self.random_translation = random_translation
        self.random_rotation = random_rotation

    def forward(self, coords: NDArray, center: Optional[NDArray]) -> NDArray:
        return do_random_transform(coords, center, self.random_translation, self.random_rotation)

    def get_transform(self) -> T :
        if self.random_rotation :
            quaternion = random_quaternion()
        else :
            quaternion = None
        if self.random_translation > 0.0:
            x, y, z = np.random.uniform(-random_translation, random_translation, size=(3))
            translation = jnp.array([[x,y,z]])
        else :
            translation = None
        return T(translation, quaternion)

@jit
def __do_transform(
    coords: NDArray,
    center: Union[Tuple[float, float, float], NDArray, None] = None,
    translation: Optional[NDArray] = None,
    quaternion: Optional[Q] = None,
) -> NDArray:
    if quaternion is not None :
        if center is not None :
            if jnp.shape(center) == (3,) :
                center = jnp.array([center])
            coords = apply_quaternion(coords - center, quaternion)
            coords += center
        else :
            coords = apply_quaternion(coords, quaternion)

        if translation is not None :
            coords += translation
    else :
        if translation is not None :
            coords = coords + translation
    return coords

def do_random_transform(
    coords: NDArray,
    center: Union[Tuple[float, float, float], NDArray, None] = None,
    random_translation: Optional[float] = 0.0,
    random_rotation: bool = False,
) -> NDArray:

    if random_rotation :
        quaternion = random_quaternion()
    else :
        quaternion = None

    if (random_translation is not False) and (random_translation is not None) and (random_translation > 0.0) :
        x, y, z = np.random.uniform(-random_translation, random_translation, size=(3))
        translation = jnp.array([[x,y,z]])
    else :
        translation = None
    
    return __do_transform(coords, center, translation, quaternion)
