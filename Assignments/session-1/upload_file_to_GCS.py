import urllib
import time
from google.cloud import storage


def upload_file(
    file_url,
    project_id,
    bucket_id,
    file_name,
):
    """This function is to upload a file from internet to Google Storage using Python

    Args:
        file_url (String): File's URL
        project_id (String): GCP Project ID
        bucket_id (String): GCS Bucket ID
        file_name (String): The file name in GCS
    """
    data_to_upload = urllib.request.urlopen(file_url).read()  # define the file
    storage_client = storage.Client(project=project_id)  # define the GCP project
    bucket = storage_client.get_bucket(bucket_id)  # define the GCS bucket ID
    blob = bucket.blob(file_name)  # define the intended file name
    blob.upload_from_string(data_to_upload)  # upload the file
    print("Upload processed ...")
    time.sleep(10)
    if blob.exists():
        print("The {} is uploaded successfully".format(file_name))
    else:
        print("The {} is uploaded unsuccessfully".format(file_name))
