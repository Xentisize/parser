import openpyxl

wb = openpyxl.load_workbook('discussion.xlsx')
wb.create_sheet('135013')
s = wb['135013']



with open('135013.txt') as fh:
    column = 1
    line = fh.readline()
    while line:
        values = line.split('|')
        for index, value in enumerate(values):
            s.cell(column, index + 1).value = value
        column += 1
        line = fh.readline()

wb.save("discussion.xlsx")