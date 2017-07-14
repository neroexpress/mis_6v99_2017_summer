import requests;import pprint;import os;import zipfile;import openpyxl
import sqlite3;import glob;import getpass;import fnmatch;import re
import csv;import pandas as pd; from operator import itemgetter

url = ('https://data.medicare.gov/views/bg9k-emty/files/'
      '0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2'
      'Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip')

k_url = "http://kevincrook.com/utd/hospital_ranking_focus_status.xlsx"
staging_dir_name = 'staging'
db_name = "medicare_hospital_compare.db"
Workbook = "hospital_ranking_focus_states.xlsx"
ranking_worksheet = "Hospital National Ranking"
Focus_states_worksheet = "Focus States"

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
		header = d_reader.fieldnames
	return header

def create_sql_table(table_name,Column_list,db_name):
	columns_tuple=tuple(Column_list)
	sql_drop_str = 'drop table if exists ' + table_name
	sql_create_str = 'create table if not exists ' + table_name  + str(columns_tuple)
	conn = sqlite3.connect(db_name)
	c1  =  conn.cursor()
	c1.execute(sql_drop_str)
	c1.execute(sql_create_str)
	c1.close()

def insert_values(file_name,table_name,Column_list,db_name):
	columns_tuple=tuple(Column_list)
	conn = sqlite3.connect(db_name)
	c1  =  conn.cursor()
	with open(file_name, "rt",encoding='cp1252') as f:
		d_reader = csv.DictReader(f)
		for line in d_reader:
			sql_tuple = tuple([line[col] for col in d_reader.fieldnames])
			blank = (sql_tuple.count(None) == len(sql_tuple)-1)
			sql_str = 'insert into ' +  table_name + str(columns_tuple) + ' values'+ str(sql_tuple)
			try:
				if blank is not True:c1.execute(sql_str)
			except Exception as e:
				raise e
	conn.commit()
	c1.close()

def creat_sqlite_db(staging_dir_name,db_name):
	glob_dir = os.path.join(staging_dir_name,"*.csv")
	for file_name in glob.glob(glob_dir):
		print(file_name)
		#print("  basename:",os.path.basename(file_name))
		header = read_header(file_name)
		#print("before: ",header)
		table_name = transform_name(os.path.splitext(os.path.basename(file_name))[0],'table')
		#print("table_name: ",table_name)
		Column_list = list()
		for head in header:
			head = transform_name(head,'column')
			Column_list.append(head)
		#print("Column_list: ",Column_list)
		create_sql_table(table_name,Column_list,db_name)
		print("Table Created: ", table_name)
		insert_values(file_name,table_name,Column_list,db_name)
		print("Values inserted: ", table_name)
		print("")
		#print("  split extension: ",os.path.splitext(os.path.basename(file_name)))
	    #print("  directory name: ", os.path.dirname(file_name))
	    #print("  absolute path: ", os.path.abspath(file_name))

def check_if_number_of_rows_matches(staging_dir_name,db_name):
	glob_dir = os.path.join(staging_dir_name,"*.csv")
	for file_name in glob.glob(glob_dir):
		with open(file_name, "rt",encoding='cp1252') as f:
			reader = csv.reader(f,delimiter = ",")
			data = list(reader)
			row_count = len(data)
			#print(row_count)
		table_name = transform_name(os.path.splitext(os.path.basename(file_name))[0],'table')
		conn = sqlite3.connect(db_name)
		c1  =  conn.cursor()
		sql_str = "select count(*) from " + table_name
		rows = c1.execute(sql_str)
		for row in rows:
		    #print(row[0])
		    pass
		numberOfRowsIntable = row[0]
		numberOfRowsInCSV = row_count-1
		print("Table: {0}, CSV: {1}".format(numberOfRowsIntable,numberOfRowsInCSV))
		if numberOfRowsIntable != numberOfRowsInCSV:
			print("Rows not equal for CSV :{0}, Table: {1}".format(file_name,table_name))
		else:print("Number of rows matches in CSV and Table")
		print("")
		c1.close()

get_Medicare_Hospital_Compare_Data(staging_dir_name,url)
get_House_Proprietary_Hospital_Rankings(k_url)
creat_sqlite_db(staging_dir_name,db_name)
check_if_number_of_rows_matches(staging_dir_name,db_name)

#--------------------------------------------------------------------------------
#-------------------------Create Hospital Ranking Excel file --------------------
#--------------------------------------------------------------------------------

hospital_ranking_workbook  = 'hospital_ranking.xlsx'
nationwide_worksheet = 'Nationwide'

def get_top_100_providerID(Workbook,ranking_worksheet):
	wb = openpyxl.load_workbook(Workbook)
	sheet = wb.get_sheet_by_name(ranking_worksheet)
	i= 1;j=0
	top_100_provider_ID = list()
	while sheet.cell(row=i,column=1).value != None and j <=100:
		#print(sheet.cell(row=i,column=1).value, "|", sheet.cell(row=i,column=2).value)
		top_100_provider_ID.append((sheet.cell(row=i,column=1).value,))
		i +=1;j +=1
	top_100_provider_ID = top_100_provider_ID[1::]
	return top_100_provider_ID

#top_100_provider_ID = get_top_100_providerID(Workbook,ranking_worksheet)
#pprint.pprint(top_100_provider_ID)
#print(len(top_100_provider_ID))

def get_details_top_100_hospitals(db_name,top_100_provider_ID):
	conn = sqlite3.connect(db_name)
	c1  =  conn.cursor()
	top_100_hospital_list = list()
	for x in top_100_provider_ID:
		sql_str = '''select provider_id, hospital_name,city,state,county_name 
					 from hospital_general_information 
					 Where provider_id = ?'''
		sql_tuple = x
		top_100_hospital_list.append(list(c1.execute(sql_str,sql_tuple).fetchone()))
	return top_100_hospital_list

top_100_hospital_detail = get_details_top_100_hospitals(db_name,get_top_100_providerID(Workbook,ranking_worksheet))
#pprint.pprint(top_100_hospital_detail)
#print(len(top_100_hospital_detail))

def create_hospital_ranking_xlsx(hospital_ranking_workbook,nationwide_worksheet,top_100_hospital_detail):
	wb2 = openpyxl.Workbook()
	sheet_1 = wb2.create_sheet(nationwide_worksheet)
	wb2.remove_sheet(wb2.get_sheet_by_name("Sheet"))
	sheet_1.cell(row=1,column=1,value="Provider ID")
	sheet_1.cell(row=1,column=2,value="Hospital Name")
	sheet_1.cell(row=1,column=3,value="City")
	sheet_1.cell(row=1,column=4,value="State")
	sheet_1.cell(row=1,column=5,value="County")
	for r_idx, row in enumerate(top_100_hospital_detail, 2):
		for c_idx, value in enumerate(row, 1):
			sheet_1.cell(row=r_idx, column=c_idx, value=value)
	wb2.save(hospital_ranking_workbook)

def get_list_of_states(Workbook,Focus_states_worksheet):
	wb = openpyxl.load_workbook(Workbook)
	sheet = wb.get_sheet_by_name(Focus_states_worksheet)
	i= 1
	list_of_Focus_states = list()
	while sheet.cell(row=i,column=1).value != None:
		list_of_Focus_states.append((sheet.cell(row=i,column=1).value,sheet.cell(row=i,column=2).value))
		i +=1
	list_of_Focus_states = list_of_Focus_states[1::]
	return list_of_Focus_states

#list_of_Focus_states = get_list_of_states(Workbook,Focus_states_worksheet)
#pprint.pprint(list_of_Focus_states)

def get_top_state_providerID_list(Workbook,ranking_worksheet,state_providerID_list):
	wb = openpyxl.load_workbook(Workbook)
	sheet = wb.get_sheet_by_name(ranking_worksheet)
	providerID_of_Focus_states = list()
	for x in state_providerID_list:
		i= 1
		while sheet.cell(row=i,column=1).value != None:
			if sheet.cell(row=i,column=1).value == x:
				providerID_of_Focus_states.append(list((sheet.cell(row=i,column=1).value,sheet.cell(row=i,column=2).value)))
			i +=1
	providerID_of_Focus_states.sort(key=itemgetter(1))
	providerID_of_Focus_states = [(row[0],) for row in providerID_of_Focus_states[0:100:]]
	#pprint.pprint(providerID_of_Focus_states)
	#print(len(providerID_of_Focus_states))
	return providerID_of_Focus_states

def create_state_ranking_worksheet(hospital_ranking_workbook,statewide_worksheet,top_100_state_hospital_Detail):
	wb3 = openpyxl.load_workbook(hospital_ranking_workbook)
	sheet_1 = wb3.create_sheet(statewide_worksheet)
	sheet_1.cell(row=1,column=1,value="Provider ID")
	sheet_1.cell(row=1,column=2,value="Hospital Name")
	sheet_1.cell(row=1,column=3,value="City")
	sheet_1.cell(row=1,column=4,value="State")
	sheet_1.cell(row=1,column=5,value="County")
	for r_idx, row in enumerate(top_100_state_hospital_Detail, 2):
		for c_idx, value in enumerate(row, 1):
			sheet_1.cell(row=r_idx, column=c_idx, value=value)
	wb3.save(hospital_ranking_workbook)

def create_state_worksheets():
	conn = sqlite3.connect(db_name)
	c1  =  conn.cursor()
	for x in get_list_of_states(Workbook,Focus_states_worksheet):
		sql_str = '''select provider_id 
					 from hospital_general_information 
					 Where state = ?'''
		sql_tuple = (x[1],)
		#rows = c1.execute(sql_str,sql_tuple)
		state_providerID_list = [row[0] for row in c1.execute(sql_str,sql_tuple)]
		#print(x[0],len(state_providerID_list))
		#pprint.pprint(state_providerID_list)
		#print("")
		top_100_state_providerID_list = get_top_state_providerID_list(Workbook,ranking_worksheet,state_providerID_list)
		top_100_state_hospital_Detail = get_details_top_100_hospitals(db_name,top_100_state_providerID_list)
		create_state_ranking_worksheet(hospital_ranking_workbook,x[0],top_100_state_hospital_Detail)


create_hospital_ranking_xlsx(hospital_ranking_workbook,nationwide_worksheet,top_100_hospital_detail)
create_state_worksheets()

#-------------------------------------------------------------------------------
#--------- Measures Statistical Analysis MS Excel Workbook----------------------
#-------------------------------------------------------------------------------






