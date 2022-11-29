import urllib
from google.cloud import storage

client = storage.Client()

"""
filedata = urllib.urlopen('http://example.com/myfile.txt')
datatoupload = filedata.read()

bucket = client.get_bucket('bucket-id-here')
blob = Blob("myfile.txt", bucket)
blob.upload_from_string(datatoupload)    
"""
