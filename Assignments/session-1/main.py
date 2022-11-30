from upload_file_to_GCS import upload_file
import warnings

warnings.filterwarnings("ignore")


def main():
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
