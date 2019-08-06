from openpyxl import load_workbook
import os
from excel_func import *
from sql_func import *

def create_protocol(id_form):
    table_path = input('Input table path:')[1:-1]  # substring for drag and drop into console
    file_name = os.path.splitext(os.path.basename(table_path))[0]
    protocols = {}
    # operation with excel
    wb = load_workbook(table_path)
    parse_excel_workbook(protocols, wb) # get data from excel
    check_null_excel_sheet(protocols)
    # operation with database oracle
    connection = connect_MED()
    sql_cursor = connection.cursor()
    parent_id = sql_get_id_form(connection, id_form)
    for protocol_name, protocol_value in protocols.items():
        if len(protocols) == 1:
            protocol_name = file_name
        try:
            add_form_string, code_form = sql_create_form(connection, parent_id, protocol_name)
            sql_cursor.execute(add_form_string)
            id = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                                 "code = '{code_form}'"
                                                 " and rownum = 1".format(code_form=code_form)).fetchone()[0])
        except Exception as e:
            print(str(protocol_name))
            print('----------------------------------------------------------------------------------')
            print(e)
            print('----------------------------------------------------------------------------------')
            input("Print enter to exist")
            continue

        for index, item_name in enumerate(protocol_value):
            try:
                sql_insert_form_item(sql_cursor, id, index, item_name)
                get_if_form_item = int(
                    connection.cursor().execute("SELECT SOLUTION_MED.PKG_GLOBAL.GET_NEXT_ID('SOLUTION_FORM',"
                                                " 'FORM_ITEM') - 1 FROM DUAL").fetchone()[0])
            except Exception as e:
                print(str(protocol_name) + ' :' + str(item_name))
                print('----------------------------------------------------------------------------------')
                print(e)
                print('----------------------------------------------------------------------------------')
                input("Press enter to continue")
                continue

            if item_name[2] == 2:
                    for index, answer in enumerate(item_name[4]):
                        try:
                            get_if_form_item_value = int(
                                connection.cursor().execute("SELECT SOLUTION_MED.PKG_GLOBAL.GET_NEXT_ID('SOLUTION_FORM',"
                                                            " 'FORM_ITEM_VALUE') FROM DUAL").fetchone()[0])
                            sql_insert_form_item_value(answer, sql_cursor, get_if_form_item, get_if_form_item_value,
                                                       index)
                        except Exception as e:
                            print(str(protocol_name) + ' : ' + str(item_name) + ' : ' + str(answer))
                            print('----------------------------------------------------------------------------------')
                            print(e)
                            print('----------------------------------------------------------------------------------')
                            input("Print enter to exist")
                            continue


if __name__ == '__main__':
    '''
        input example
        C:\\Users\ARM2\Desktop\Исследование функции внешнего дыхания.xlsx
        11222242
    '''
    id_form = input('Input code parent form:')
    while True:
        create_protocol(id_form)