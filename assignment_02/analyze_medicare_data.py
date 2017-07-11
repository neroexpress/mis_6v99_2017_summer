import requests
import pprint
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass

url = "https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"

url

r = requests.get(url)

(r.headers)

r.headers['content-type']

type(r.content)

staging_dir_name = 'staging'
if (os.path.isdir(staging_dir_name)) is False:os.mkdir(staging_dir_name)

os.path.isdir(staging_dir_name)

zip_file_name = os.path.join(staging_dir_name,"test.zip")

zip_file_name

zf = open(zip_file_name,'wb')
zf.write(r.content)

zf.close()

z = zipfile.ZipFile(zip_file_name,'r')
z.extractall(staging_dir_name)
z.close()