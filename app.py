from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
import os
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Retrieve the storage connection string from the environment
        conn_str = os.environ.get('STORAGE_CONNECTION_STRING')
        if not conn_str:
            return render_template('error.html', 
                error_title="Configuration Error",
                error_message="STORAGE_CONNECTION_STRING environment variable is not set.",
                error_details="Please set the STORAGE_CONNECTION_STRING environment variable in your app configuration.")

        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)

        # Create a container
        container_name = 'mycontainer'
        container_client = blob_service_client.get_container_client(container_name)
        try:
            container_client.create_container()
        except Exception as container_error:
            # Container might already exist, which is fine
            pass

        # Upload a blob
        blob_name = 'test.txt'
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob('Hello from the web app!', overwrite=True)

        # Retrieve the blob content
        blob_content = blob_client.download_blob().readall().decode('utf-8')

        return render_template('index.html', blob_content=blob_content)
    except Exception as e:
        error_traceback = traceback.format_exc()
        return render_template('error.html', 
            error_title="Application Error",
            error_message=str(e),
            error_details=error_traceback)

if __name__ == '__main__':
    app.run()   