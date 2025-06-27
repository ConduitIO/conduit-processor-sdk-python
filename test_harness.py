import sdk
import processor as user_processor # Import the user's processor file

from proto.opencdc.v1 import opencdc_pb2
from proto.processor.v1 import processor_pb2

def main():
    """
    A simple test harness to simulate the Conduit Wasm host.
    It manually calls the exported functions in the SDK to test the processor.
    """

    print("--- Test Harness Initializing ---")
    # In a real scenario, the Wasm runtime would instantiate the module,
    # which would call sdk.run() with the SimpleProcessor instance.
    # We simulate that here.
    print(f"Loaded processor: {user_processor.SimpleProcessor.specification(None).name}")


    print("\n--- Simulating a 'process' call (expecting ACK) ---")
    # 1. Create a test record
    record_in = opencdc_pb2.Record(
        position=b'1',
        operation=opencdc_pb2.OPERATION_CREATE,
        metadata={"source": "test-harness"},
        payload=opencdc_pb2.Change(after=opencdc_pb2.Data(raw_data=b'{"foo":"bar"}'))
    )
    print(f"Input Record:\n{record_in}")

    # 2. Wrap it in a ProcessRequest, serialize it, and write to memory
    request = processor_pb2.ProcessRequest(record=record_in)
    packed_req_ptr = sdk.write_to_memory(request.SerializeToString())

    # 3. Call the SDK's process function (this is what the host does)
    packed_resp_ptr = sdk.process(packed_req_ptr)

    # 4. Read the response from memory and deserialize it
    resp_bytes = sdk.read_from_memory(packed_resp_ptr)
    response = processor_pb2.ProcessResponse()
    response.ParseFromString(resp_bytes)

    # 5. Inspect the response
    if response.HasField("record"):
        print("✅ Result: ACK")
        print(f"Processed Record:\n{response.record}")
    else:
        print("❌ Unexpected Result!")


    print("\n--- Simulating a 'process' call (expecting FILTER) ---")
    record_in_filter = opencdc_pb2.Record(
        position=b'2',
        operation=opencdc_pb2.OPERATION_UPDATE,
        metadata={"over_threshold": "true"},
        payload=opencdc_pb2.Change(after=opencdc_pb2.Data(raw_data=b'{"foo":"baz"}'))
    )
    print(f"Input Record:\n{record_in_filter}")

    request_filter = processor_pb2.ProcessRequest(record=record_in_filter)
    packed_req_ptr_filter = sdk.write_to_memory(request_filter.SerializeToString())

    packed_resp_ptr_filter = sdk.process(packed_req_ptr_filter)

    resp_bytes_filter = sdk.read_from_memory(packed_resp_ptr_filter)
    response_filter = processor_pb2.ProcessResponse()
    response_filter.ParseFromString(resp_bytes_filter)

    if response_filter.HasField("filter"):
        print("✅ Result: FILTER")
    else:
        print("❌ Unexpected Result!")

if __name__ == "__main__":
    main()
