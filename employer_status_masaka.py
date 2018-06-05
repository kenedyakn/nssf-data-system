import xlrd
import mysql.connector
import pandas as pd
import sqlalchemy

database_username = 'phpmyadmin'
database_password = '123!@#QWEasd'
database_ip = 'localhost'
database_name = 'nssf_db'
database_table = 'employers'

conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                               database=database_name)

workbook = xlrd.open_workbook('employer_status_masaka.xlsx')

print("Number of sheets: {0}".format(workbook.nsheets))
print("Sheet names: {0}".format(workbook.sheet_names()))

sheet = workbook.sheet_by_name('Brenda')

print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))

# for rx in range(sheet.nrows):
#     print(sheet.row(rx))

total_rows = sheet.nrows
total_cols = sheet.ncols

record = list()
table = list()


cursor = conn.cursor()
query = 'insert into '+database_table+' (employer_number, employer_name, nssf_number) values'

print(query)

try:
    cursor.execute('insert into operators(first_name,last_name,auth_id,dob,password) '
                   'values(\'' + first_name + '\',\'' + last_name + '\',\'' + auth_id + '\',\'' + date_of_birth + '\''
                                                                                                                  ',\'' + password + '\')')
    conn.commit()
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
    conn.rollback()

for x in range(1, total_rows):
    for y in range(7):
        record.append(str(sheet.cell(x, y).value))
    print('(', str(record[0]), ',', str(record[1]), ',', str(record[2]),')')
    record = []
    x += 1

'''
df = pd.read_excel('employer_status_masaka.xlsx', 3)

df.columns = df.columns.str.lower()

database_username = 'phpmyadmin'
database_password = '123!@#QWEasd'
database_ip = 'localhost'
database_name = 'nssf_db'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))
df.to_sql(con=database_connection, name='table_name_for_df', if_exists='append')

# df.to_sql(con=conn, name='table_name_for_df', if_exists='replace')


# full_df = df
#
# new_df = full_df[['Employer Number', 'Employer Name', 'NSSF Number', 'Month Last paid',
#  'Amount Paid']].copy()
#
# print(new_df.columns.values)
'''
