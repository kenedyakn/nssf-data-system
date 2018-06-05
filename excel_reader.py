import xlrd

workbook = xlrd.open_workbook('ecollection_report.xlsx')

print(workbook.nsheets)
print("Worksheet name(s): {0}".format(workbook.sheet_names()))

sheet = workbook.sheet_by_index(0)
print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))

print("Cell G04 is {0}".format(sheet.cell_value(rowx=3, colx=6)))

for rx in range(sheet.nrows):
    print(sheet.row(rx))

print('\n\n')

total_rows = sheet.nrows
total_cols = sheet.ncols

record = list()
table = list()

for x in range(total_rows):
    for y in range(total_cols):
        record.append(sheet.cell(x, y).value)
    table.append(record)
    record = []
    x += 1

print(table)
