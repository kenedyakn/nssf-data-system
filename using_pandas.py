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