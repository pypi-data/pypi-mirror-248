# ain_storage/sdk.py
import grpc
import p2p_file_system_pb2
import p2p_file_system_pb2_grpc
import directory_service_pb2
import directory_service_pb2_grpc

class AinStorage:
    def __init__(self, directory_server_address):
        self.directory_server_address = directory_server_address
        # ... Other initialization ...

    def upload_file(self, filename, file_data, node_address):
        # ... Implementation of file upload ...
        
    def download_file(self, filename, save_path, node_address):
        # ... Implementation of file download ...

    def _update_directory_server(self, filename, node_address):
        # ... Implementation for updating the directory server ...
