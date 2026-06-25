from hdfs import InsecureClient
import os

class HDFSManager:
    def __init__(self, host='192.168.56.101', port=50070, user='cloudera'):
        """Initialize HDFS Client (WebHDFS)"""
        self.url = f'http://{host}:{port}'
        self.client = InsecureClient(self.url, user=user)
        print(f"Connected to HDFS at {self.url}")

    def upload_file(self, local_path, hdfs_path):
        """Upload a local file to HDFS"""
        try:
            if not os.path.exists(local_path):
                print(f"Error: Local file {local_path} does not exist.")
                return False
            
            self.client.upload(hdfs_path, local_path, overwrite=True)
            print(f"Successfully uploaded {local_path} to {hdfs_path}")
            return True
        except Exception as e:
            print(f"Failed to upload: {e}")
            return False

    def list_files(self, hdfs_dir='/'):
        """List files in an HDFS directory"""
        try:
            files = self.client.list(hdfs_dir)
            print(f"Files in {hdfs_dir}: {files}")
            return files
        except Exception as e:
            print(f"Failed to list files: {e}")
            return []

    def makedirs(self, hdfs_dir):
        """Create a directory in HDFS"""
        try:
            self.client.makedirs(hdfs_dir)
            print(f"Created HDFS directory: {hdfs_dir}")
        except Exception as e:
            print(f"Failed to create directory: {e}")

if __name__ == "__main__":
    # Quick test
    hdfs = HDFSManager()
    hdfs.list_files('/user/cloudera')
