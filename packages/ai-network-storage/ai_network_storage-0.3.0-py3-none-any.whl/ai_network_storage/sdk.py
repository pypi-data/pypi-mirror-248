# ai_network_storage/sdk.py
import grpc
import os
from p2p_file_system_pb2_grpc import P2PFileServiceStub
from p2p_file_system_pb2 import FileRequest, FileChunk
from directory_service_pb2_grpc import DirectoryServiceStub
from directory_service_pb2 import FileLocationUpdate

class AINetworkStorageSDK:
    def __init__(self, directory_server_address):
        self.directory_server_address = directory_server_address

    def _get_directory_stub(self):
        return DirectoryServiceStub(grpc.insecure_channel(self.directory_server_address))

    def upload_file(self, node_address, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            data = file.read()

        with grpc.insecure_channel(node_address) as channel:
            stub = P2PFileServiceStub(channel)
            def file_chunk_generator():
                with open(file_path, 'rb') as file:
                    while True:
                        piece = file.read(1024)  # Read in chunks of 1KB
                        if not piece:
                            break
                        yield FileChunk(filename=file_path, data=piece)
            response = stub.UploadFile(file_chunk_generator())
            print (response)

        # Update the directory server
        directory_stub = self._get_directory_stub()
        directory_stub.UpdateFileLocation(FileLocationUpdate(filename=filename, node_addresses=[node_address]))
        print(f"File '{filename}' uploaded to node {node_address}")

    def download_file(self, node_address, filename, save_path):
        with grpc.insecure_channel(node_address) as channel:
            stub = P2PFileServiceStub(channel)
            file_stream = stub.DownloadFile(FileRequest(filename=filename))

            with open(save_path, 'wb') as file:
                for data in file_stream:
                    file.write(data.data)

        print(f"File '{filename}' downloaded from node {node_address}")

# Example usage
if __name__ == "__main__":
    sdk = AINetworkStorageSDK("localhost:50052")
    sdk.upload_file("localhost:50053", "sample.txt")
    sdk.download_file("localhost:50053", "example.txt", "exmple.txt")


# Example usage remains the same
