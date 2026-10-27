"""Verify stored commitments and deterministic proof without an SDK or model."""
import hashlib
import json
import sys
from pathlib import Path

# Load pure helpers only; the contract's SDK imports and class are not executed.
source=(Path(__file__).resolve().parents[1]/'contracts/alias_guard.py').read_text()
source=source[source.index('import json'):source.index('class AliasGuard')]
ns={}
exec(compile(source,'alias_guard_helpers','exec'),ns)
record=json.loads(Path(sys.argv[1]).read_text())
assert record['input_hash']==ns['digest']({'version':ns['VERSION'],'input':record['input']})
assert record['proof']==ns['derive'](record['relations'],len(record['input']['entries']))
assert record['assessment_hash']==ns['digest']({'input_hash':record['input_hash'],'relations':record['relations'],'proof':record['proof']})
assert record['state'] == ('PUBLISHED' if 'certificate' in record else record['proof']['state'])
if record['state']=='PUBLISHED':
    assert record['certificate']==ns['certificate'](record)
    assert record['certificate_hash']==ns['digest'](record['certificate'])
print('PASS: input, graph proof, assessment and publication commitments independently recomputed.')
