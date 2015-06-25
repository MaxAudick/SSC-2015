#! /usr/bin/python

import time
from max import recursiveFact

tick = time.time()
print recursiveFact(600)
print time.time() - tick
