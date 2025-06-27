import os
import sys

# Add the 'proto' directory to the Python path.
# This must be done BEFORE importing the sdk or processor.
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

import sdk
# Import the class from the renamed simple_processor.py
from simple_processor import SimpleProcessor

from opencdc.v1 import opencdc_pb2
from processor.v1 import processor_pb2

def main():
    """
    A simple test harness to simulate the Conduit Wasm host.
    """
    print("--- Test Harness Initializing ---")
    
    # 1. Instantiate the user's processor class.
    processor_instance = SimpleProcessor()
    
    # 2. Register the instance with the SDK.
    sdk.run(processor_instance)
    
    print(f"Loaded processor: {sdk.PROCESSOR.specification().name}")

    print("\n--- Simulating a 'process' call with 2 records (1 ACK, 1 FILTER) ---")
    
    records_in = [
        opencdc_pb2.Record(
            position=b'1',
            operation=opencdc_pb2.OPERATION_CREATE,
            metadata={"source": "test-harness"},
            payload=opencdc_pb2.Change(after=opencdc_pb2.Data(raw_data=b'{"foo":"bar"}'))
        ),
        opencdc_pb2.Record(
            position=b'2',
            operation=opencdc_pb2.OPERATION_UPDATE,
            metadata={"over_threshold": "true"},
            payload=opencdc_pb2.Change(after=opencdc_pb2.Data(raw_data=b'{"foo":"baz"}'))
        )
    ]
    print(f"Input Records:\n{records_in}")

    request = processor_pb2.Process.Request(records=records_in)
    packed_req_ptr = sdk.write_to_memory(request.SerializeToString())
    packed_resp_ptr = sdk.process(packed_req_ptr)

    resp_bytes = sdk.read_from_memory(packed_resp_ptr)
    response = processor_pb2.Process.Response()
    response.ParseFromString(resp_bytes)

    print(f"\nHost received ProcessResponse with {len(response.records)} results:")
    
    rec1_resp = response.records[0]
    if rec1_resp.HasField("single_record"):
        print("✅ Record 1 Result: ACK")
        print(f"   Processed Record:\n{rec1_resp.single_record}")
        assert "processed-by" in rec1_resp.single_record.metadata
    else:
        print(f"❌ Record 1 Unexpected Result! Got: {rec1_resp}")

    rec2_resp = response.records[1]
    if rec2_resp.HasField("filter_record"):
        print("✅ Record 2 Result: FILTER")
    else:
        print(f"❌ Record 2 Unexpected Result! Got: {rec2_resp}")

if __name__ == "__main__":
    main()
