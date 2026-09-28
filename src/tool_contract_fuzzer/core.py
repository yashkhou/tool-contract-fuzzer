from __future__ import annotations
import random

def value(schema,rng):
    if 'enum' in schema: return rng.choice(schema['enum'])
    t=schema.get('type','object')
    if t=='object': return {k:value(v,rng) for k,v in schema.get('properties',{}).items() if k in schema.get('required',[]) or rng.random()>.35}
    if t=='array':
        lo=schema.get('minItems',0); hi=min(schema.get('maxItems',3),3); return [value(schema.get('items',{}),rng) for _ in range(rng.randint(lo,max(lo,hi)))]
    if t=='string': return 's'+str(rng.randint(0,9999))
    if t=='integer': return rng.randint(schema.get('minimum',0),schema.get('maximum',100))
    if t=='number': return round(rng.random()*10,3)
    if t=='boolean': return bool(rng.getrandbits(1))
    return None

def invalid_variants(schema,good):
    out=[]; t=schema.get('type')
    if t=='object' and isinstance(good,dict):
        for k in schema.get('required',[]):
            if k in good:
                x=dict(good); x.pop(k); out.append(('missing-required:'+k,x))
        if good:
            k=next(iter(good)); x=dict(good); x[k]={'wrong':'type'}; out.append(('wrong-type:'+k,x))
    elif t=='array': out.append(('wrong-type',{'not':'array'}))
    else: out.append(('wrong-type',[]))
    return out

def cases(schema,seed=0,count=10):
    rng=random.Random(seed)
    for i in range(count):
        good=value(schema,rng); yield {'id':f'valid-{i}','valid':True,'value':good}
        for reason,bad in invalid_variants(schema,good): yield {'id':f'invalid-{i}-{reason}','valid':False,'value':bad}

def shrink(obj,predicate):
    cur=obj
    while True:
        if isinstance(cur,dict): opts=[{k:v for k,v in cur.items() if k!=drop} for drop in list(cur)]
        elif isinstance(cur,list): opts=[cur[:i]+cur[i+1:] for i in range(len(cur))]
        elif isinstance(cur,str) and len(cur)>1: opts=[cur[:max(1,len(cur)//2)]]
        elif isinstance(cur,int) and cur: opts=[cur//2,0]
        else: opts=[]
        nxt=next((x for x in opts if predicate(x)),None)
        if nxt is None: return cur
        cur=nxt
