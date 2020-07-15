import illustris_python as il
import numpy as np

cluster = il.groupcat.loadSubhalos("/data/TNG300-2/output/", 99,
                                   fields=['GroupGasMetallicity'])
