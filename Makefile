PROTO_DIR = proto
PROTO_FILE = $(PROTO_DIR)/hub.proto

.PHONY: proto clean

proto:
	@echo "Generating gRPC code from $(PROTO_FILE)..."
	python -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		$(PROTO_FILE)
	@echo "Done!"

clean:
	rm -f $(PROTO_DIR)/*_pb2.py $(PROTO_DIR)/*_pb2_grpc.py
