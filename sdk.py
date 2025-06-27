# sdk.py
import sys
from typing import Dict, Optional

# Import generated protobuf files
from proto.processor.v1 import processor_pb2
from proto.opencdc.v1 import opencdc_pb2
from proto.config.v1 import parameter_pb2

# Global instance of the user-defined processor
PROCESSOR: Optional['Processor'] = None

# --- Memory Management ---
# In a real Wasm environment, these functions would be provided by the runtime
# or implemented to interact with the Wasm linear memory.
def write_to_memory(data: bytes) -> int:
    """Writes bytes to memory, returns a packed ptr-size uint64."""
    size = len(data)
    # In real wasm, you'd call an exported malloc function
    ptr = _malloc(size)
    # And then write to the memory view
    _get_memory_view()[ptr:ptr+size] = data
    return (ptr << 32) | size

def read_from_memory(packed_ptr: int) -> bytes:
    """Reads bytes from a packed ptr-size uint64."""
    ptr = packed_ptr >> 32
    size = packed_ptr & 0xFFFFFFFF
    return _get_memory_view()[ptr:ptr+size]

# --- Processor Interface ---
# This is the interface the user will implement.
class Processor:
    def specification(self) -> 'Specification':
        raise NotImplementedError
    def configure(self, config_map: Dict[str, str]):
        pass  # Optional
    def open(self):
        pass  # Optional
    def process(self, record: opencdc_pb2.Record) -> 'ProcessResult':
        raise NotImplementedError
    def teardown(self):
        pass  # Optional

# --- SDK Data Structures ---
# These are helper classes for the user.
class Specification:
    def __init__(self, name: str, version: str, summary: str, description: str, author: str, params: Dict[str, parameter_pb2.Parameter]):
        self.name, self.version, self.summary, self.description, self.author, self.params = name, version, summary, description, author, params

class ProcessResult:
    # Factory methods for creating results
    @staticmethod
    def Ack(record: opencdc_pb2.Record) -> 'ProcessResult': return ProcessResult(record=record)
    @staticmethod
    def Filter() -> 'ProcessResult': return ProcessResult(filter=True)
    @staticmethod
    def Error(err: Exception) -> 'ProcessResult': return ProcessResult(error=err)

    def __init__(self, record=None, filter=False, error=None):
        self.record, self.filter, self.error = record, filter, error


# --- Wasm Exported Functions ---
# These are the functions called by the Conduit host. They handle the
# request/response protocol. The user does not need to know about them.

def export(name):
    def decorator(func):
        setattr(func, '_export_name', name)
        # In a real toolchain (e.g. wasmer-python), this would register the export
        return func
    return decorator

@export("conduit.processor.v1.specification")
def specification(packed_ptr: int) -> int:
    # No request body for spec
    spec_model = PROCESSOR.specification()
    response = processor_pb2.SpecificationResponse(
        name=spec_model.name,
        version=spec_model.version,
        summary=spec_model.summary,
        description=spec_model.description,
        author=spec_model.author,
        parameters=spec_model.params
    )
    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.configure")
def configure(packed_ptr: int) -> int:
    req_bytes = read_from_memory(packed_ptr)
    request = processor_pb2.ConfigureRequest()
    request.ParseFromString(req_bytes)
    PROCESSOR.configure(request.config)
    return 0 # No response body

@export("conduit.processor.v1.open")
def open_processor(packed_ptr: int) -> int:
    # No request body for open
    PROCESSOR.open()
    return 0 # No response body

@export("conduit.processor.v1.process")
def process(packed_ptr: int) -> int:
    req_bytes = read_from_memory(packed_ptr)
    request = processor_pb2.ProcessRequest()
    request.ParseFromString(req_bytes)
    result = PROCESSOR.process(request.record)

    response = processor_pb2.ProcessResponse()
    if result.error:
        response.error.message = str(result.error)
    elif result.filter:
        response.filter.SetInParent()
    else:
        response.record.CopyFrom(result.record)

    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.teardown")
def teardown(packed_ptr: int) -> int:
    # No request body for teardown
    PROCESSOR.teardown()
    return 0 # No response body

# --- SDK Entrypoint ---
def run(processor: Processor):
    """
    Sets the global processor instance. The Wasm host will then call
    the exported functions on this instance.
    """
    global PROCESSOR
    if not isinstance(processor, Processor):
        raise TypeError("argument must be an instance of sdk.Processor")
    PROCESSOR = processor

# Dummy implementations for memory management for standalone testing
# In a real Wasm environment, these would be provided by the host/runtime.
_WASM_MEMORY = bytearray(1024 * 128) # 128KB
_OFFSET = 0
def _malloc(size):
    global _OFFSET
    ptr = _OFFSET
    _OFFSET += size
    return ptr
def _get_memory_view():
    return _WASM_MEMORY
