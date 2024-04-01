import numpy as np
import numpy.testing as npt


def test_IsTriangle():
    from glass.core.misc import tri, isTriangle

    arr = np.array([1, 2, 3, 4, 5])
    vfunc = np.vectorize(tri)
    triangles = vfunc(arr)
    for element in triangles:
        print("element = " + str(element))
        assert isTriangle(element) is True