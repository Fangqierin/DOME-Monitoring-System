import os

import numpy

print(os.getcwd())

from FQ_Firesim_Testbed import output

print(output(
    numpy.asarray(
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
    )
))
