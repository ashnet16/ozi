PROTO_DIR = proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

.PHONY: proto clean

proto:
	@echo "Generating gRPC code from: $(PROTO_FILES)"
	python -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		$(PROTO_FILES)
	@echo "Done!"

clean:
	rm -f $(PROTO_DIR)/*_pb2.py $(PROTO_DIR)/*_pb2_grpc.py
