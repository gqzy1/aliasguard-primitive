"""Official SDK storage and serialization checks; model and host consensus are mocked."""
import json
from pathlib import Path
from gltest.direct import VMContext, deploy_contract, create_address

root=Path(__file__).resolve().parents[1]
vm=VMContext()
vm.sender=create_address('aliasguard-sdk-test')
with vm.activate():
    contract=deploy_contract(root/'contracts/alias_guard.py',vm,sdk_version='v0.2.16')
    vm.check_pickling=True
    vm.mock_llm('.*',json.dumps({'relations':['SAME','DIFFERENT','DIFFERENT']}))
    key=contract.seal('equipment',(root/'examples/equipment.json').read_text())
    result=json.loads(contract.assess(key,0))
    assert result['state']=='READY'
    result=json.loads(contract.publish(key,1))
    assert result['state']=='PUBLISHED'
    assert result['certificate']['groups']==[{'canonical':0,'members':[0,1]},{'canonical':2,'members':[2]}]
    assert json.loads(contract.get_record(key))==result
    print('PASS: official SDK storage, calldata, callback serialization and lifecycle; mocked model, no network consensus.')
