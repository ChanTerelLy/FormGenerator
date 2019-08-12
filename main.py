from openpyxl import load_workbook
import os
from excel_func import *
from except_func import *
from sql_func import *


def create_protocol(id_form, table_path=None):
    if not table_path:
        table_path = input('Input table path:')[1:-1]  # substring for drag and drop into console
    file_name = os.path.splitext(os.path.basename(table_path))[0]
    protocols = {}
    exception_count = 0
    # operation with excel
    try:
        wb = load_workbook(table_path)
        protocols = check_null_excel_sheet(parse_excel_workbook(wb)) # get data from excel
    except Exception as e:
        exception_count = +1
        print('Check excel parse block')
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
                id = sql_get_id_by_code(code_form, connection)
            except Exception as e:
                print('Problem with creation FORM')
                exception_count=+1
                print(str(protocol_name))
                print_exception(e)
                continue

            for index, item_name in enumerate(protocol_value):
                try:
                    sql_insert_form_item(sql_cursor, id, index, item_name)
                    id_form_item = sql_get_id_form_item(sql_cursor)
                except Exception as e:
                    print('Problem with insert form_item')
                    exception_count = +1
                    print(str(protocol_name) + ' :' + str(item_name))
                    print_exception(e)
                    continue

                if item_name[2] == 2:
                    for index, answer in enumerate(item_name[4]):
                        try:
                            id_form_item_value = sql_get_id_form_item_value(connection)
                            sql_insert_form_item_value(answer, sql_cursor, id_form_item, id_form_item_value,
                                                       index)
                        except Exception as e:
                            print('Problem with insert form_item_value')
                            exception_count = +1
                            print(str(protocol_name) + ' : ' + str(item_name) + ' : ' + str(answer))
                            print_exception(e)
                            continue
    except Exception as e:
        print('Problem with DATABASE')
        exception_count = +1
        print_exception(e)
    print('Exception_count: ', exception_count)
    print('Success')


def CMD_fast_creating(connection):
    print(sql_get_all_protocol_folders(connection))  # get all folders forms
    choice_create_form = input('Create form: yes/no ')
    if choice_create_form == 'yes':
        form_name = input('Input form name:')
        sql_create_parent_form(connection, form_name)
        print(sql_get_all_protocol_folders(connection))
    id_form = input('Input code parent form:')
    while True:
        create_protocol(id_form)


if __name__ == '__main__':
    connection, sql_cursor = connect_MED()
    CMD_fast_creating(connection)
