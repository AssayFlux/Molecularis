"""Deterministic workflow DAG construction and validation smoke benchmark."""
from __future__ import annotations
import argparse,json,time
from molecularis.platform import Capability,MolecularisPlatform
from molecularis.workflows_service import WorkflowDocument,WorkflowOperation,validate_workflow

def run(steps:int)->dict[str,object]:
    if not 1<=steps<=100: raise ValueError("steps must be 1..100")
    platform=MolecularisPlatform(":memory:"); platform.start()
    try:
        operations=[]; previous="source"
        for index in range(steps):
            capability=f"bench.step{index}.v1"
            platform.register(Capability(capability,"1","benchmark","pass","input","output"))
            platform.bind(capability,lambda inputs,parameters,context:{"ok":True})
            output=f"result{index}"; operations.append(WorkflowOperation(f"step{index}",capability,(previous,),output)); previous=output
        workflow=WorkflowDocument("benchmark",tuple(operations),("source",))
        started=time.perf_counter(); report=validate_workflow(platform,workflow)
        return {"steps":steps,"validated_steps":report["operation_count"],"elapsed_seconds":time.perf_counter()-started}
    finally: platform.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--steps",type=int,default=50)
    print(json.dumps(run(parser.parse_args().steps),sort_keys=True))
