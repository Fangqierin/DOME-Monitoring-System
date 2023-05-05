import os
import sys

import numpy

sys.path.insert(0,
                'D://Workplace/Projects/courses/cs295p/DOME-An-end-to-end-drone-based-platform-for-monitoring-emerging-events/task2/server_script/DOMETestbed')
os.chdir('DOMETestbed')

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
