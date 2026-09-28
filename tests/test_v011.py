import json, random, unittest
from tool_contract_fuzzer.core import cases, invalid_variants, value
class BoundaryTests(unittest.TestCase):
    def test_valid_generation_honors_bounds(self):
        schema={'type':'object','required':['n','name'],'properties':{'n':{'type':'integer','minimum':5,'maximum':8},'name':{'type':'string','minLength':3,'maxLength':5}}}
        rng=random.Random(7)
        for _ in range(20):
            x=value(schema,rng); self.assertTrue(5<=x['n']<=8); self.assertTrue(3<=len(x['name'])<=5)
    def test_invalid_mutations_probe_boundaries(self):
        schema={'type':'object','additionalProperties':False,'required':['n'],'properties':{'n':{'type':'integer','minimum':2,'maximum':4}}}
        reasons={r for r,_ in invalid_variants(schema,{'n':3})}
        self.assertTrue({'below-minimum:n','above-maximum:n','additional-property'}<=reasons)
    def test_generated_cases_remain_json_serializable(self):
        schema={'type':'object','required':['x'],'properties':{'x':{'type':'string','const':'fixed'}}}
        json.dumps(list(cases(schema,seed=1,count=1)))
    def test_seed_deterministic(self):
        s={'type':'integer','minimum':1,'maximum':9}; self.assertEqual(list(cases(s,42,4)),list(cases(s,42,4)))
if __name__=='__main__': unittest.main()
