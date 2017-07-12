import requests
import pprint
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass
import fnmatch
import re
import csv

url = ('https://data.medicare.gov/views/bg9k-emty/files/'
      '0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2'
      'Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip')

k_url = "http://kevincrook.com/utd/hospital_ranking_focus_status.xlsx"
staging_dir_name = 'staging'

def get_Medicare_Hospital_Compare_Data(staging_dir_name,url):
	r = requests.get(url)
	if (os.path.isdir(staging_dir_name)) is False:os.mkdir(staging_dir_name)
	zip_file_name = os.path.join(staging_dir_name,"test.zip")
	zf = open(zip_file_name,'wb')
	zf.write(r.content)
	zf.close()
	z = zipfile.ZipFile(zip_file_name,'r')
	z.extractall(staging_dir_name)
	z.close()
	os.remove(os.path.join(staging_dir_name,"FY2015_Percent_Change_in_Medicare_Payments.csv"))
	#print(len(fnmatch.filter(os.listdir(staging_dir_name),'*.csv')))

def get_House_Proprietary_Hospital_Rankings(k_url):
	r = requests.get(k_url)
	xf = open("hospital_ranking_focus_states.xlsx","wb")
	xf.write(r.content)
	xf.close()

#get_Medicare_Hospital_Compare_Data(staging_dir_name,url)
#get_House_Proprietary_Hospital_Rankings(k_url)

def transform_name(file_name,tb):
	#print("Earlier: ",file_name)
	file_name = file_name.lower()
	file_name = re.sub(r'[\s\-\/]',"_",file_name)
	file_name = re.sub(r'%',"pct",file_name)
	if tb =='table':
		file_name = re.sub(r'^[^a-zA-Z]+',"t_",file_name)
	else:
		file_name = re.sub(r'^[^a-zA-Z]+',"c_",file_name)
	#print("Later: ",file_name)
	return file_name

def read_header(file_name):
	with open(file_name, "rt",encoding='cp1252') as f:
		d_reader = csv.DictReader(f)
		headers = d_reader.fieldnames
	return headers

glob_dir = os.path.join(staging_dir_name,"*.csv")
conn = sqlite3.connect("test.db")
c1  =  conn.cursor()

for file_name in glob.glob(glob_dir):
	print(file_name)
	#print("  basename:",os.path.basename(file_name))
	header = read_header(file_name)
	#print("before: ",header)
	table_name = transform_name(os.path.splitext(os.path.basename(file_name))[0],'table')
	print("table_name: ",table_name)
	Column_list = list()
	for head in header:
		head = transform_name(head,'column')
		Column_list.append(head)
	print("Column_list: ",Column_list)
	print("")
	#print("  split extension: ",os.path.splitext(os.path.basename(file_name)))
    #print("  directory name: ", os.path.dirname(file_name))
    #print("  absolute path: ", os.path.abspath(file_name))



'''
wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")

for sheet_name in wb.get_sheet_names():
    print(sheet_name)

sheet = wb.get_sheet_by_name("Hospital National Ranking")

i= 1
while sheet.cell(row=i,column=1).value != None:
    print(sheet.cell(row=i,column=1).value, "|", sheet.cell(row=i,column=2).value)
    i +=1

sheet = wb.get_sheet_by_name("Focus States")

i= 1
while sheet.cell(row=i,column=1).value != None:
    print(sheet.cell(row=i,column=1).value, "|", sheet.cell(row=i,column=2).value)
    i +=1

wb2 = openpyxl.Workbook()

sheet_1 = wb2.create_sheet("utd")

sheet_1.cell(row=1,column=1,value="buan")

for i in range(2,11):
    sheet_1.cell(row=i,column=1,value=i-1)

sheet_2 = wb2.create_sheet("test")
sheet_2.cell(row=1,column=2,value="valued")

wb2.remove_sheet(wb2.get_sheet_by_name("Sheet"))

wb2.save("test.xlsx")

openpyxl.__version__

'''

'''
sql_str = "drop table if exists my_table"
c1.execute(sql_str)

sql_str = '''
#create table if not exists my_table(
#column_1 text,
#column_2 text,
#column_3 text)
'''

c1.execute(sql_str)

sql_str = "insert into my_table(column_1,column_2,column_3) values(?,?,?)"
sql_tuple = ('a','b','c')
c1.execute(sql_str,sql_tuple)

conn.commit()

sql_str= "select * from my_table"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "select * from sqlite_master"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "PRAGMA table_info('my_table')"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "select * from sqlite_master where tbl_name = ?"
sql_tuple = ('my_table',)
c1.execute(sql_str,sql_tuple)
for row in rows:
    print(row)

sql_str = "select count(*) from my_table"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

#zip_file_name = os.path.join(staging_dir_name,"test.zip")

#fn = "Timely and Effective Care - Hospital.csv"
fn= os.path.join(staging_dir_name,"Timely and Effective Care - Hospital.csv")
in_fp = open(fn,'rt',encoding='cp1252')
input_data = in_fp.read()
in_fp.close()

ofn= os.path.join(staging_dir_name,"Timely and Effective Care - Hospital.csv")
out_fp = open(ofn,'wt',encoding='utf-8')
for c in input_data:
    if c != '\0':
        out_fp.write(c)
out_fp.close()

github_username = input("Enter your github username: ")

github_password = getpass.getpass("enter your password")

github_url = "https://api.github.com/user/repos"

r = requests.get(github_url,auth=(github_username,github_password))

r.status_code

r.json()

r.headers

'''


#--- Code for getting excel file from the internet----


k_url = "http://kevincrook.com/utd/hospital_ranking_focus_status.xlsx"

k_url

r = requests.get(k_url)

r.headers

xf = open("hospital_ranking_focus_states.xlsx","wb")



xf.write(r.content)

xf.close()

wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")

for sheet_name in wb.get_sheet_names():
    print(sheet_name)

sheet = wb.get_sheet_by_name("Hospital National Ranking")

i= 1
while sheet.cell(row=i,column=1).value != None:
    print(sheet.cell(row=i,column=1).value, "|", sheet.cell(row=i,column=2).value)
    i +=1

sheet = wb.get_sheet_by_name("Focus States")

i= 1
while sheet.cell(row=i,column=1).value != None:
    print(sheet.cell(row=i,column=1).value, "|", sheet.cell(row=i,column=2).value)
    i +=1

wb2 = openpyxl.Workbook()

sheet_1 = wb2.create_sheet("utd")

sheet_1.cell(row=1,column=1,value="buan")

for i in range(2,11):
    sheet_1.cell(row=i,column=1,value=i-1)

sheet_2 = wb2.create_sheet("test")
sheet_2.cell(row=1,column=2,value="valued")

wb2.remove_sheet(wb2.get_sheet_by_name("Sheet"))

wb2.save("test.xlsx")

openpyxl.__version__

conn = sqlite3.connect("test.db")

c1  =  conn.cursor()

sql_str = "drop table if exists my_table"
c1.execute(sql_str)



sql_str = '''
create table if not exists my_table(
column_1 text,
column_2 text,
column_3 text)
'''

c1.execute(sql_str)

sql_str = "insert into my_table(column_1,column_2,column_3) values(?,?,?)"
sql_tuple = ('a','b','c')
c1.execute(sql_str,sql_tuple)

conn.commit()

sql_str= "select * from my_table"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "select * from sqlite_master"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "PRAGMA table_info('my_table')"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

sql_str = "select * from sqlite_master where tbl_name = ?"
sql_tuple = ('my_table',)
c1.execute(sql_str,sql_tuple)
for row in rows:
    print(row)

sql_str = "select count(*) from my_table"
rows = c1.execute(sql_str)
for row in rows:
    print(row)

#zip_file_name = os.path.join(staging_dir_name,"test.zip")

#fn = "Timely and Effective Care - Hospital.csv"
fn= os.path.join(staging_dir_name,"Timely and Effective Care - Hospital.csv")
in_fp = open(fn,'rt',encoding='cp1252')
input_data = in_fp.read()
in_fp.close()

ofn= os.path.join(staging_dir_name,"Timely and Effective Care - Hospital.csv")
out_fp = open(ofn,'wt',encoding='utf-8')
for c in input_data:
    if c != '\0':
        out_fp.write(c)
out_fp.close()

glob_dir = os.path.join(staging_dir_name,"*.csv")
for file_name in glob.glob(glob_dir):
    print(file_name)
    print("  basename:",os.path.basename(file_name))
    print("  split extension: ",os.path.splitext(os.path.basename(file_name)))
    print("  directory name: ", os.path.dirname(file_name))
    print("  absolute path: ", os.path.abspath(file_name))

github_username = input("Enter your github username: ")

github_password = getpass.getpass("enter your password")

github_url = "https://api.github.com/user/repos"

r = requests.get(github_url,auth=(github_username,github_password))

r.status_code

r.json()

r.headers









