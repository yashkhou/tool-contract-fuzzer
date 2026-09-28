import argparse,json
from .core import cases
ap=argparse.ArgumentParser(); ap.add_argument('schema'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=5); a=ap.parse_args()
for c in cases(json.load(open(a.schema)),a.seed,a.count): print(json.dumps(c,sort_keys=True))
