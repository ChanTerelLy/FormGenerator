from openpyxl import load_workbook
import os
from excel_func import *
from except_func import *
from sql_func import *
import argparse


def create_protocol(id_form, table_path=None):
    if not table_path:
        table_path = input('Input table path:')[1:-1]  # substring for drag and drop into console
    file_name = os.path.splitext(os.path.basename(table_path))[0]
    protocols = {}
    # operation with excel
    try:
        wb = load_workbook(table_path)
        protocols = parse_excel_workbook(wb)  # get data from excel
        check_null_excel_sheet(protocols)
    except Exception as e:
        print_exception(e)
    # operation with database oracle
    try:
        connection, sql_cursor = connect_MED()
        parent_id = sql_get_id_form(connection, id_form)
        for protocol_name, protocol_value in protocols.items():
            if len(protocols) == 1:
                protocol_name = file_name
            try:
                code_form = sql_create_children_form(connection, parent_id, protocol_name)
                id = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                                     "code = '{code_form}'"
                                                     " and rownum = 1".format(code_form=code_form)).fetchone()[0])
            except Exception as e:
                print(str(protocol_name))
                print_exception(e)
                continue

            for index, item_name in enumerate(protocol_value):
                try:
                    sql_insert_form_item(sql_cursor, id, index, item_name)
                    get_if_form_item = int(
                        connection.cursor().execute("SELECT SOLUTION_MED.PKG_GLOBAL.GET_NEXT_ID('SOLUTION_FORM',"
                                                    " 'FORM_ITEM') - 1 FROM DUAL").fetchone()[0])
                except Exception as e:
                    print(str(protocol_name) + ' :' + str(item_name))
                    print_exception(e)
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
                            print_exception(e)
                            continue
    except Exception as e:
        print_exception(e)
    print(exception_count)
    print('Success')


if __name__ == '__main__':
    connection, sql_cursor = connect_MED()
    print(sql_get_all_protocol_folders(connection)) # get all folders forms
    choice_create_form = input('Create form: yes/no ')
    if choice_create_form == 'yes':
        form_name  = input('Input form name:')
        sql_create_parent_form(connection, form_name)
        print(sql_get_all_protocol_folders(connection))
    id_form = input('Input code parent form:')
    while True:
        create_protocol(id_form)
