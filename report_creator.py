"""Reporting script for warehouse"""

# Imports

import argparse
import sqlite3
import xlsxwriter


# Constants
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Read DataBase
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def readfile(file):
    """ Reading Sql query file

    Args:
        file (str): path to query

    Returns:
        str: query
    """
    with open(file, "r", encoding='utf-8') as sql:
        return " ".join([line.strip() for line in sql.readlines()])

# Write report

def write_hat(worksheet, startpoint, prev_unit):
    """
    Function creates new header in table
    """

    # HARDCODE
    # HARDCODE

    worksheet.write(f'D{startpoint[1]}', prev_unit)
    #_______________________________________________
    worksheet.write(f'A{startpoint[1]+1}', "№ з/п")
    worksheet.write(f'B{startpoint[1]+1}', \
"Найменування, стисла характеристика та призначення об’єкта")
    worksheet.write(f'C{startpoint[1]+1}', \
"Рік випуску (будівництва) чи дата придбання (введення в експлуатацію) та виготовлювач")
    worksheet.write(f'D{startpoint[1]+1}', "Номер")
    worksheet.write(f'G{startpoint[1]+1}', "Один. виміру")
    worksheet.write(f'H{startpoint[1]+1}', "Фактична наявність")
    worksheet.write(f'J{startpoint[1]+1}', "Відмітка про вибуття")
    worksheet.write(f'K{startpoint[1]+1}', "За даними бухгалтерського обліку")
    worksheet.write(f'P{startpoint[1]+1}', "Інші відомості")
    #________________________________________________
    worksheet.write(f'D{startpoint[1]+2}', "інвентарний/номенклатурний")
    worksheet.write(f'E{startpoint[1]+2}', "заводський")
    worksheet.write(f'F{startpoint[1]+2}', "паспорта")
    worksheet.write(f'H{startpoint[1]+2}', "кількість")
    worksheet.write(f'I{startpoint[1]+2}', "первісна (переоцінена) вартість")
    worksheet.write(f'K{startpoint[1]+2}', "кількість")
    worksheet.write(f'L{startpoint[1]+2}', "первісна (переоцінена) вартість")
    worksheet.write(f'M{startpoint[1]+2}', "сума зносу (накопиченої амортизації)")
    worksheet.write(f'N{startpoint[1]+2}', "балансова вартість")
    worksheet.write(f'O{startpoint[1]+2}', "строк корисного використання")
    #_____________________________________________________
    for i in range(16):
        worksheet.write(f"{LETTERS[startpoint[0]+i]}{startpoint[1]+3}", i+1)
    #_____________________________________________________
    startpoint = (startpoint[0], startpoint[1]+4)

    return startpoint, startpoint[1]

def write_data(worksheet, row, startpoint, start_count):
    """
    Function writes data into table
    """

    worksheet.write(f'A{startpoint[1]}', f"=A{start_count}+1")
    worksheet.write(f'B{startpoint[1]}', row['name'])
    worksheet.write(f'C{startpoint[1]}', "2024")
    worksheet.write(f'D{startpoint[1]}', row['id'])
    worksheet.write(f'E{startpoint[1]}', "")
    worksheet.write(f'G{startpoint[1]}', row['measurement_unit'])
    worksheet.write(f'H{startpoint[1]}', row['quantity'])
    worksheet.write(f'I{startpoint[1]}', row['price'])
    worksheet.write(f'K{startpoint[1]}', row['sumquant'])
    worksheet.write(f'L{startpoint[1]}', row['price'])
    worksheet.write(f'M{startpoint[1]}', row['amortization'])
    worksheet.write(f'N{startpoint[1]}', f'=L{startpoint[1]}-M{startpoint[1]}')



    if startpoint[1] > 5:
        start_count = startpoint[1]
    else:
        worksheet.write(f'A7', 1)
    return (startpoint[0], startpoint[1]+1), start_count

def write_foot(worksheet, startpoint, sum_index):
    """
    Function creates new footer in table
    """
    worksheet.write(f'A{startpoint[1]}', "Разом")
    worksheet.write(f'B{startpoint[1]}', 'x')
    worksheet.write(f'C{startpoint[1]}', 'x')
    worksheet.write(f'D{startpoint[1]}', 'x')
    worksheet.write(f'E{startpoint[1]}', 'x')
    worksheet.write(f'F{startpoint[1]}', 'x')
    worksheet.write(f'G{startpoint[1]}', 'x')
    worksheet.write(f'H{startpoint[1]}', f"=SUM(H{sum_index}:H{startpoint[1]-1})")
    worksheet.write(f'I{startpoint[1]}', f"=SUM(I{sum_index}:I{startpoint[1]-1})")
    worksheet.write(f'K{startpoint[1]}', f"=SUM(K{sum_index}:K{startpoint[1]-1})")
    worksheet.write(f'L{startpoint[1]}', f"=SUM(L{sum_index}:L{startpoint[1]-1})")
    worksheet.write(f'M{startpoint[1]}', f"=SUM(M{sum_index}:M{startpoint[1]-1})")
    worksheet.write(f'N{startpoint[1]}', f"=SUM(N{sum_index}:N{startpoint[1]-1})")
    worksheet.write(f'O{startpoint[1]}', 'x')
    worksheet.write(f'P{startpoint[1]}', 'x')
    concat = f"=CONCATENATE(\"Усі цінності, пронумеровані в цьому інвентаризаційному описі з N \",TEXT(A{sum_index}, \"0\"),\" до N \",TEXT(A{startpoint[1]-1}, \"0\"),\", перевірено комісією в натурі в моїй присутності та внесено в опис. У зв'язку з цим претензій до інвентаризаційної комісії не маю. Цінності, перелічені в описі, знаходяться на моєму відповідальному зберіганні.\")"
    worksheet.write_formula(f'A{startpoint[1]+1}', f'{concat}')
    worksheet.write(f'A{startpoint[1]+2}', "Матеріально відповідальна особа:")
    worksheet.write(f'A{startpoint[1]+3}', '"___"')
    worksheet.write(f'B{startpoint[1]+3}', "___________________")
    worksheet.write(f'C{startpoint[1]+3}', '20____ р.')
    worksheet.write(f'F{startpoint[1]+4}', '(посада)')
    worksheet.write(f'I{startpoint[1]+4}', '(підпис)')
    worksheet.write(f'L{startpoint[1]+4}', '(ініціали, прізвище)')


    return (startpoint[0], startpoint[1]+5)

def main(args):
    """Creates file for report

    Returns:
        Worksheet of report
    """

    con = sqlite3.connect(args.inputfile)
    con.row_factory = dict_factory
    cur = con.cursor()
    if args.outfile:
        workbook = xlsxwriter.Workbook(args.outfile)
    else:
        workbook = xlsxwriter.Workbook("example.xlsx")
    worksheet = workbook.add_worksheet()

    startpoint = (0, 1)

    prev_unit = None

    if args.sqlfile:
        query = readfile(args.sqlfile)
    else:
        query = "SELECT u.short_name, e.name, e.id, \
        e.measurement_unit, op.quantity, SUM(op.quantity) as sumquant, \
        SUM(op.quantity)*e.price as price, SUM(op.quantity)*e.amortization as amortization \
        FROM operations op LEFT JOIN units u ON op.unit_id = u.id LEFT \
        JOIN equipment e ON op.equipment_id = e.id GROUP BY op.unit_id, \
        op.equipment_id;"

    start_count = 5

    for row in cur.execute(query):
        if prev_unit is None:
            prev_unit = row['short_name']
            startpoint, sum_index = write_hat(worksheet, startpoint, prev_unit)
        if prev_unit != row['short_name']:
            startpoint = write_foot(worksheet, startpoint, sum_index)
            prev_unit = row['short_name']
            startpoint, sum_index = write_hat(worksheet, startpoint, prev_unit)
        startpoint, start_count= write_data(worksheet, row, startpoint, start_count)

        print(row)
    write_foot(worksheet, startpoint, sum_index)
    
    print(startpoint)
    # startpoint = write_data(worksheet, startpoint)
    # startpoint = write_foot(worksheet, startpoint)

    workbook.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='report_creator',
        description='',
        epilog=''
    )
    parser.add_argument('inputfile', help="path to database")
    parser.add_argument('-o','--outfile', help="path to output <.xlsx> | default <example.xlsx>")
    parser.add_argument('-s', '--sqlfile', help="path to sql query file <.sql> | default query")

    args = parser.parse_args()
    main(args)
