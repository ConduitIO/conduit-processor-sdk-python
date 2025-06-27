PYTHON := python3
PIP := $(PYTHON) -m pip

deps:
	@echo "Installing dependencies..."
	@$(PIP) install protobuf~=6.31.1
	@$(PIP) install types-protobuf~=6.30
	@$(PIP) install googleapis-common-protos~=1.70.0


.PHONY: proto
proto:
	@echo "Generating protobuf Python files..."
	@cd proto; buf generate buf.build/conduitio/conduit-commons --template buf.gen.yaml
	@cd proto; buf generate buf.build/conduitio/conduit-processor-sdk --template buf.gen.yaml
	@echo "Creating __init__.py files..."
	@find proto -type d -exec touch {}/__init__.py \;

