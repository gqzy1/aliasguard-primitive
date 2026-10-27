"""Scripted host tests. No model inference, node or network consensus."""
import itertools
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

class Return:
    def __init__(self, value): self.calldata = value

class Map(dict):
    @classmethod
    def __class_getitem__(cls, item): return cls

host = types.SimpleNamespace(message=types.SimpleNamespace(sender_address='0xabc'),
    public=types.SimpleNamespace(view=lambda f:f, write=lambda f:f), Contract=object,
    vm=types.SimpleNamespace(Return=Return), nondet=types.SimpleNamespace())
module = types.ModuleType('genlayer')
module.__all__ = ['gl','TreeMap','u32']
module.gl, module.TreeMap, module.u32 = host, Map, int
namespace = {}
with patch.dict(sys.modules, {'genlayer':module}):
    exec(compile((Path(__file__).resolve().parents[1]/'contracts/alias_guard.py').read_text(), 'alias_guard.py', 'exec'), namespace)
G = types.SimpleNamespace(**namespace)
FIXTURE = json.loads((Path(__file__).resolve().parents[1]/'examples/equipment.json').read_text())

class Algorithm(unittest.TestCase):
    def test_all_729_four_entry_graphs(self):
        n=4
        for labels in itertools.product(['SAME','DIFFERENT','UNKNOWN'], repeat=6):
            closure=[[a==b for b in range(n)] for a in range(n)]
            for (a,b),v in zip(G.pairs(n),labels):
                if v=='SAME': closure[a][b]=closure[b][a]=True
            for k in range(n):
                for a in range(n):
                    for b in range(n): closure[a][b] |= closure[a][k] and closure[k][b]
            bad=[[a,b] for (a,b),v in zip(G.pairs(n),labels) if closure[a][b] and v=='DIFFERENT']
            missing=[[a,b] for (a,b),v in zip(G.pairs(n),labels) if not closure[a][b] and v=='UNKNOWN']
            out=G.derive(list(labels),n)
            self.assertEqual(out['state'],'CONFLICT' if bad else 'UNRESOLVED' if missing else 'READY')
            self.assertEqual([x['different'] for x in out['conflicts']],bad)
            self.assertEqual(out['unresolved'],missing)
            self.assertEqual(sorted(sum(out['components'],[])),list(range(n)))
            mapping=dict(zip(G.pairs(n),labels))
            for witness in out['conflicts']+out['inferred']:
                path=witness['same_path']
                target=witness.get('different',witness.get('pair'))
                self.assertEqual([path[0],path[-1]],target)
                for a,b in zip(path,path[1:]): self.assertEqual(mapping[tuple(sorted([a,b]))],'SAME')
    def test_contradiction_path(self):
        out=G.derive(['SAME','DIFFERENT','SAME'],3)
        self.assertEqual(out['conflicts'],[{'different':[0,2],'same_path':[0,1,2]}])
    def test_unknown_inside_closure_is_explicit_inference(self):
        out=G.derive(['SAME','UNKNOWN','SAME'],3)
        self.assertEqual(out['state'],'READY')
        self.assertEqual(out['inferred'],[{'pair':[0,2],'same_path':[0,1,2]}])
    def test_cross_group_unknown_blocks(self):
        self.assertEqual(G.derive(['SAME','DIFFERENT','UNKNOWN'],3)['state'],'UNRESOLVED')
    def test_isolated_and_maximum_bounds(self):
        self.assertEqual(G.derive(['DIFFERENT']*15,6)['components'],[[i] for i in range(6)])
        self.assertEqual(G.derive(['SAME']*15,6)['components'],[list(range(6))])
    def test_canonical_shortest_path(self):
        self.assertEqual(G.same_path([[1,2],[0,3],[0,3],[1,2]],0,3),[0,1,3])

class Validation(unittest.TestCase):
    def test_payload(self): self.assertEqual(G.input_data(json.dumps(FIXTURE)),FIXTURE)
    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(Exception,'DUPLICATE_JSON_KEY'): G.decode('{"x":1,"x":2}')
    def test_entry_bounds_and_duplicates(self):
        for value in [[],['a'], ['x'*10]*2, ['x'*601,'y'*10]]:
            with self.assertRaises(Exception): G.input_data(json.dumps({'scope':'catalogue scope','entries':value}))
    def test_invalid_strings(self):
        for value in [' leading space','trailing space ','control\x00text','\ud800xxxxxxxxxx']:
            with self.assertRaises(Exception): G.bounded_text(value,10,600)
    def test_model_schema(self):
        for value in [{'relations':['SAME']}, {'relations':['SAME',True,'SAME']}, {'relations':['same']*3}, {'relations':['SAME']*3,'reason':'yes'}, '```json\n{}\n```']:
            with self.assertRaises(Exception): G.decision(value,3)
    def test_equivalence_independent_all_pairs(self):
        calls=[]
        def independent(): calls.append(1); return {'relations':['SAME','DIFFERENT','DIFFERENT']}
        self.assertTrue(G.equivalent(Return(independent()),independent,3))
        self.assertEqual(len(calls),2)
        self.assertFalse(G.equivalent(Return({'relations':['SAME','DIFFERENT','UNKNOWN']}),independent,3))
    def test_errors_and_nonreturn_fail_closed(self):
        self.assertFalse(G.equivalent(object(),lambda:None,3))
        self.assertFalse(G.equivalent(Return({'relations':['SAME']*3}),lambda:1/0,3))

class Lifecycle(unittest.TestCase):
    def setUp(self):
        host.message.sender_address='0xabc'
        self.contract=G.AliasGuard()
        self.contract.records=Map(); self.contract.counts=Map()
        self.labels=['SAME','DIFFERENT','DIFFERENT']
        host.nondet.exec_prompt=lambda *a,**k: json.dumps({'relations':self.labels})
        def consensus(leader,validator):
            value=leader()
            if not validator(Return(value)): raise Exception('CONSENSUS_REJECTED')
            return value
        host.vm.run_nondet_unsafe=consensus
        self.key=self.contract.seal('equipment',json.dumps(FIXTURE))
    def test_complete_lifecycle(self):
        assessed=json.loads(self.contract.assess(self.key,0))
        self.assertEqual(assessed['state'],'READY')
        out=json.loads(self.contract.publish(self.key,1))
        self.assertEqual(out['certificate']['groups'],[{'canonical':0,'members':[0,1]},{'canonical':2,'members':[2]}])
        self.assertEqual(out['certificate_hash'],G.digest(out['certificate']))
        self.assertEqual(json.loads(self.contract.get_record(self.key)),out)
    def test_idempotent_seal_and_conflict(self):
        self.assertEqual(self.contract.seal('equipment',json.dumps(FIXTURE)),self.key)
        other=dict(FIXTURE,scope='Different catalogue scope')
        with self.assertRaisesRegex(Exception,'ID_CONFLICT'): self.contract.seal('equipment',json.dumps(other))
    def test_owner_isolation(self):
        host.message.sender_address='0xdef'
        with self.assertRaisesRegex(Exception,'OWNER_ONLY'):self.contract.assess(self.key,0)
        self.assertNotEqual(self.contract.seal('equipment',json.dumps(FIXTURE)),self.key)
    def test_revision(self):
        with self.assertRaisesRegex(Exception,'STALE_REVISION'):self.contract.assess(self.key,1)
    def test_nonexistent(self):
        self.assertEqual(self.contract.get_record('absent'),'')
        with self.assertRaisesRegex(Exception,'NOT_FOUND'):self.contract.assess('absent',0)
    def test_no_publish_before_consensus(self):
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.contract.publish(self.key,0)
    def test_unresolved_cannot_publish(self):
        self.labels=['UNKNOWN']*3
        self.assertEqual(json.loads(self.contract.assess(self.key,0))['state'],'UNRESOLVED')
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.contract.publish(self.key,1)
    def test_conflict_cannot_publish(self):
        self.labels=['SAME','DIFFERENT','SAME']
        self.assertEqual(json.loads(self.contract.assess(self.key,0))['state'],'CONFLICT')
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.contract.publish(self.key,1)
    def test_failed_consensus_preserves_record(self):
        before=self.contract.get_record(self.key)
        def fail(a,b): raise Exception('CONSENSUS_REJECTED')
        host.vm.run_nondet_unsafe=fail
        with self.assertRaises(Exception): self.contract.assess(self.key,0)
        self.assertEqual(before,self.contract.get_record(self.key))
    def test_validator_rejects_changed_pair(self):
        before=self.contract.get_record(self.key)
        def disagree(a,b):
            proposal=a(); self.labels=['SAME','DIFFERENT','UNKNOWN']
            if not b(Return(proposal)): raise Exception('CONSENSUS_REJECTED')
            return proposal
        host.vm.run_nondet_unsafe=disagree
        with self.assertRaisesRegex(Exception,'CONSENSUS_REJECTED'):self.contract.assess(self.key,0)
        self.assertEqual(before,self.contract.get_record(self.key))
    def test_terminal_and_one_assessment(self):
        self.contract.assess(self.key,0)
        with self.assertRaisesRegex(Exception,'ALREADY_ASSESSED'):self.contract.assess(self.key,1)
        self.contract.publish(self.key,1)
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.contract.publish(self.key,2)
    def test_tampered_proof(self):
        r=json.loads(self.contract.assess(self.key,0));r['proof']['components']=[[0,1,2]]
        self.contract.records[self.key]=G.pack(r)
        with self.assertRaisesRegex(Exception,'NOT_READY'):self.contract.publish(self.key,1)
    def test_quota(self):
        for i in range(15):self.contract.seal('new-'+str(i),json.dumps(FIXTURE))
        with self.assertRaisesRegex(Exception,'OWNER_LIMIT'):self.contract.seal('over-limit',json.dumps(FIXTURE))
    def test_bad_slug(self):
        for slug in ['X','bad/slug','a'*33]:
            with self.assertRaisesRegex(Exception,'SLUG'):self.contract.seal(slug,json.dumps(FIXTURE))

if __name__=='__main__':unittest.main()
