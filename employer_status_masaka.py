import xlrd
import mysql.connector
import pandas as pd
import sqlalchemy
import re
import math

database_username = 'phpmyadmin'
database_password = '123!@#QWEasd'
database_ip = 'localhost'
database_name = 'nssf_db'
employers_table = 'employers'

conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                               database=database_name)

wbook = xlrd.open_workbook('excel_data/employer_status_masaka.xlsx')


# print("Number of sheets: {0}".format(workbook.nsheets))
# print("Sheet names: {0}".format(workbook.sheet_names()))


# print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))

# for rx in range(sheet.nrows):
#     print(sheet.row(rx))


def process_workbook(workbook):
    sheets = workbook.sheet_names()
    process_sheets(workbook, sheets)


def process_sheets(workbook, sheets):
    for sheet_name in sheets:
        sheet = workbook.sheet_by_name(sheet_name)
        total_rows = sheet.nrows
        total_cols = sheet.ncols
        process_data(sheet, total_rows, total_cols)


def process_data(sheet, total_rows, total_cols):
    add_to_db(sheet, total_rows, total_cols)


def is_available(param):
    cursor = conn.cursor()
    is_available = False
    query = 'select employer_number from ' + employers_table + ' where employer_number = \'' + param + '\' limit 1'
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    count = len(rows)
    if count > 0:
        is_available = True
    return is_available


def add_to_db(sheet, rows, cols):
    cursor = conn.cursor()
    total_rows = rows
    total_cols = cols
    record = list()
    table = list()
    try:
        query = 'insert into ' + employers_table + ' (employer_number, employer_name, nssf_number) values'
        values = ''
        full_query = ''
        for x in range(1, total_rows):
            for y in range(7):
                record.append(str(sheet.cell(x, y).value))
            values = '(\'' + str(record[0]).strip() + '\',\'' + re.escape(str(record[1]).strip()) + '\',\'' + str(
                record[2]).strip() + '\')'
            # if s != '':
            #     s = s[:s.index('.')]
            #     print(s)

            full_query = query + values
            if is_available(str(record[0])):
                print("{0} is available".format(str(record[0])))
            else:
                cursor.execute(full_query)
            record = []
            x += 1

        conn.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()


process_workbook(wbook)
