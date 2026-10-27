// Example only: import and call these helpers with a locally managed signer.
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionStatus,TransactionHashVariant} from 'genlayer-js/types';
export function clientFor(account) { return createClient({chain:studionet,account}); }
export async function readRecord(client,address,id) {
  return JSON.parse(await client.readContract({address,functionName:'get_record',args:[id],transactionHashVariant:TransactionHashVariant.LATEST_FINAL}));
}
export async function sendOnce(client,address,functionName,args) {
  if(await client.request({method:'eth_chainId',params:[]})!=='0xf22f') throw Error('Wrong chain');
  if(BigInt(await client.request({method:'eth_gasPrice',params:[]}))!==0n) throw Error('Nonzero gas price');
  const hash=await client.writeContract({address,functionName,args,value:0n,leaderOnly:false,consensusMaxRotations:0});
  console.log('Submitted hash; retain it before tracking:',hash);
  const receipt=await client.waitForTransactionReceipt({hash,status:TransactionStatus.FINALIZED,interval:5000,retries:120});
  if ((receipt.statusName ?? receipt.status_name) !== 'FINALIZED' || receipt.result_name !== 'MAJORITY_AGREE' || !receipt.consensus_data?.leader_receipt?.some(r => r.mode === 'leader' && r.execution_result === 'SUCCESS' && r.result?.status === 'return')) throw Error('Consensus/execution failed; retain hash and do not resend');
  return {hash,receipt}; // Also read back exact state before another write.
}
// seal('equipment', JSON.stringify(example)); assess(id,0); publish(id,1).
// Never automatically resend a failed or uncertain transaction. No Appeal.
