import warnings
import urllib
import time
import os
from google.cloud import storage

warnings.filterwarnings("ignore")


def upload_file(file_url, project_id, bucket_id, file_name):
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


def main():
    """The main function"""
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./application_default_credentials.json"
    my_url = "https://example-files.online-convert.com/document/txt/example.txt"
    my_project = "data-fellowship-8-adrian"
    my_bucket = "dummy-bucket-adrian"
    my_file_name = "sample_file.txt"

    print("The file URL is {}".format(my_url))
    print("The file name is {}".format(my_file_name))
    print("My GCP project ID is {}".format(my_project))
    print("My GCS Bucket ID is {}".format(my_bucket))
    upload_file(my_url, my_project, my_bucket, my_file_name)


if __name__ == "__main__":
    main()
