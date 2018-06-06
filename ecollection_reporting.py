import xlrd
import mysql.connector
import pandas as pd
import sqlalchemy
import re
import math
import datetime

database_username = 'phpmyadmin'
database_password = '123!@#QWEasd'
database_ip = 'localhost'
database_name = 'nssf_db'
employers_table = 'employers'
payments_table = 'payments'
collections_table = 'collections'

conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                               database=database_name)

wbook = xlrd.open_workbook('excel_data/ecollection_report_2.xlsx')

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


def add_to_db(sheet, rows, cols):
    cursor = conn.cursor()
    total_rows = rows
    total_cols = cols
    record = list()
    table = list()
    try:
        query = 'insert into ' + collections_table + ' (finance_processed, ' \
                                                   'printed_receipt, ' \
                                                   'branch_code,' \
                                                   'receipt_number,' \
                                                   'total_number_employees,' \
                                                   'parent_number_for_topup,' \
                                                   'employer_number,' \
                                                   'employer_name,' \
                                                   'description_of_payment,' \
                                                   'dl_date,' \
                                                   'receipt_date,' \
                                                   'receipt_total_amount,' \
                                                   'currency_code,' \
                                                   'cash_cheque_number,' \
                                                   'bank_transacted,' \
                                                   'bank_name,' \
                                                   'arrear_amount,' \
                                                   'number_of_arrears_a_month,' \
                                                   'arrears_paid_for,' \
                                                   'bonus_amount,' \
                                                   'address_number,' \
                                                   'bank_manual_reference_number' \
                                                   ') values'
        values = ''
        full_query = ''
        for x in range(1, total_rows):
            for y in range(total_cols):
                record.append(sheet.cell(x, y).value)

            # Processes date data
            wrongValue = record[8]
            date = ''
            try:
                workbook_datemode = wbook.datemode
                y, m, d, hh, mm, ss = xlrd.xldate_as_tuple(wrongValue, workbook_datemode)
                date = "{0}-{1}-{2}".format(y, m, d)
            except TypeError as err:
                print("No date specified")

            dl_date = str(record[9]).strip()
            receipt_date = str(record[10]).strip()


            d = dl_date.split("/")
            clean_dl_date = d[2]+'/'+d[1]+'/'+d[0]
            r = receipt_date.split("/")
            clean_receipt_date = r[2]+'/'+r[1]+'/'+r[0]
            #End processing date data


            values = '(\'' + str(record[0]).strip() + '\',\''\
                     + re.escape(str(record[1]).strip()) + '\',\'' \
                     + re.escape(str(record[2]).strip()) + '\',\'' \
                     + re.escape(str(record[3]).strip()) + '\',\'' \
                     + re.escape(str(record[4]).strip()) + '\',\'' \
                     + re.escape(str(record[5]).strip()) + '\',\'' \
                     + re.escape(str(record[6]).strip()) + '\',\'' \
                     + re.escape(str(record[7]).strip()) + '\',\'' \
                     + re.escape(str(date).strip()) + '\',\'' \
                     + re.escape(clean_dl_date.strip()) + '\',\'' \
                     + re.escape(clean_receipt_date.strip()) + '\',\'' \
                     + re.escape(str(record[11]).strip()) + '\',\'' \
                     + re.escape(str(record[12]).strip()) + '\',\'' \
                     + re.escape(str(record[13]).strip()) + '\',\'' \
                     + re.escape(str(record[14]).strip()) + '\',\'' \
                     + re.escape(str(record[15]).strip()) + '\',\'' \
                     + re.escape(str(record[16]).strip()) + '\',\'' \
                     + re.escape(str(record[17]).strip()) + '\',\'' \
                     + re.escape(str(record[18]).strip()) + '\',\'' \
                     + re.escape(str(record[19]).strip()) + '\',\'' \
                     + re.escape(str(record[21]).strip()) + '\',\'' \
                     + str(record[21]).strip() + '\')'

            full_query = query + values
            cursor.execute(full_query)
            # print(date, record[9], record[10])
            record = []
            x += 1

        conn.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()


process_workbook(wbook)
