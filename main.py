import os
import sys

# --- Path Correction ---
# Add the 'proto' directory to the Python path at runtime.
# This ensures the generated protobuf files can find their dependencies.
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))
# ---

import sdk
from simple_processor import SimpleProcessor

# `componentize-py` will generate this bindings file based on `processor.wit`
from bindings import bindings

# This class implements the interface defined in our `processor.wit` file.
class WasmProcessor(bindings.Processor):
    def conduit_processor_v1_malloc(self, size: int) -> int:
        return sdk.malloc(size)

    def conduit_processor_v1_specification(self, req_ptr_size: int) -> int:
        return sdk.specification(req_ptr_size)

    def conduit_processor_v1_configure(self, req_ptr_size: int) -> int:
        return sdk.configure(req_ptr_size)

    def conduit_processor_v1_open(self, req_ptr_size: int) -> int:
        return sdk.open_processor(req_ptr_size)

    def conduit_processor_v1_process(self, req_ptr_size: int) -> int:
        return sdk.process(req_ptr_size)

    def conduit_processor_v1_teardown(self, req_ptr_size: int) -> int:
        return sdk.teardown(req_ptr_size)

# --- Initialization ---
# This code runs when the Wasm module is instantiated by the host.
# We create an instance of our user-defined processor and register it with the SDK.
processor_instance = SimpleProcessor()
sdk.run(processor_instance)
