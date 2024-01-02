import sys

if sys.platform.startswith('win'):
    split: str = '\\'
else:
    split: str = '/'

sys.path.append(split.join(__file__.split(split)[:-2]) + split)

import tooltils
