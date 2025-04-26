.PHONY: format lint test type-check check proto clean-proto

format:
	poetry run black consumers producers rag llm
	poetry run isort consumers producers rag llm

lint:
	poetry run flake8 consumers producers rag llm

test:
	poetry run pytest

type-check:
	poetry run mypy .

check: format lint type-check

PROTO_DIR = proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

proto:
	@echo "Generating gRPC code from: $(PROTO_FILES)"
	python -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		--experimental_allow_proto3_optional \
		$(PROTO_FILES)
	@echo "Proto generation complete."

clean-proto:
	@echo "Cleaning up generated gRPC files..."
	rm -f $(PROTO_DIR)/*_pb2.py $(PROTO_DIR)/*_pb2_grpc.py
	@echo "Proto files cleaned."
