import unittest,sys; sys.path.insert(0,'src')
from tool_contract_fuzzer.core import *
S={'type':'object','required':['x'],'properties':{'x':{'type':'integer','minimum':1,'maximum':3},'y':{'type':'string'}}}
class T(unittest.TestCase):
 def test_deterministic(self): self.assertEqual(list(cases(S,4,3)),list(cases(S,4,3)))
 def test_invalid_missing(self): self.assertTrue(any(k.startswith('missing-required') for k,_ in invalid_variants(S,{'x':1})))
 def test_shrink(self): self.assertEqual(shrink({'a':1,'b':2},lambda x:'b' in x),{'b':2})
