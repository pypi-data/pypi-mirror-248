
from sdk import AINetworkStorageSDK



ssdk = AINetworkStorageSDK("34.172.161.134:50052")
ssdk.upload_file("34.172.161.134:50053", "sample.txt")
ssdk.download_file("34.172.161.134:50053", "example.txt", "exmple.txt")
