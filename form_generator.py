import cx_Oracle
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import re

# primary data
table_path = input('Input table path:')
id_form = input('Input code parent form:')
file_name = os.path.splitext(os.path.basename(table_path))[0]
'''
input example
C:\\Users\Roman\OneDrive - Северный Арктический Федеральный Университет\MED\ДКМЦ\Протоколы\ДИАГНОСТИКА\УЗИ\УЗИ 1 МЕС.xlsx
C:\\Users\ARM2\Desktop\Исследование функции внешнего дыхания.xlsx
11222242

'''

# get data from excel
wb = load_workbook(table_path)
sheets_names = []
protocol_rows = []

for ws in wb.worksheets:
    for i in range(1, 3): #check name protocol in the first three row
        if ws.cell(i, 1).value:
            sheet_name = ws.cell(i, 1).value
            sheets_names.append(sheet_name)
            break
    for row in range(5, ws.max_row): # 5 row is begin protocol_row
        element = ws.cell(row, 1).value
        # 0 - разделитель
        # 1 - редактируемый
        # 2 - невидимый
        # 3 - только
        # чтение
        # 4 - неактивный;
        element_data = ws.cell(row, 2).value
        # Исследование функции внешнего дыхания
        type_answer = ws.cell(row, 3).value
        # 0 - Простой текст (строка) 1 - Описание (много строк) 2 - Значения из списка
        # 3 - Значения из внешнего справочника 4 - Формула 5 - Таблица 6 - Значение из системного справочника
        # 7 - Формула SQL 8 - Поле для ввода диагноза 9 - Поле для ввода услуг 10 - Значение из дерева
        # 11 - Значение из списка отмеченное галочками 12 - Файл 13 - Схема (изображение);
        multi_choise = ws.cell(row, 4).value
        # 0 or 1
        answers = ws.cell(row, 5).value
        # Нарушений легочной вентиляции не зарегистрировано
        # Проба с физической нагрузкой - положительная
        if element:
            if re.search(r'Заголовок', element): #sive gramma mistakes
                element = 0
            elif re.search(r'Вопрос', element):
                element = 1
        elif element == None: # configurate unpredictable row
            element = 1
        #sive location mistakes
        else:
            element_data = element
            element = 0
        if element_data == None:
            element_data = ''
        if type_answer:
            if re.search(r'свободный ответ', type_answer) or re.search(r'простой текст', type_answer):
                type_answer = 0
            elif re.search(r'значения из списка', type_answer):
                type_answer = 2
        else:
            type_answer = 0
        if multi_choise:
            if re.match(r'нет', multi_choise) or re.match(r'-', multi_choise):
                multi_choise = 0
            elif re.match(r'да', multi_choise):
                multi_choise = 1
            else:
                multi_choise = 0
        else:
            multi_choise = 0
        if ws.cell(row, 5).value:
            answers = ws.cell(row, 5).value.split('\n')
        elif ws.cell(row, 5).value == None:
            answers = ['']

        row = [element, element_data, type_answer, multi_choise, answers]
        protocol_rows.append(row)

# operation with oracle database
connection = cx_Oracle.connect('solution_med/elsoft@med')
print(connection.version)
create_form = connection.cursor()
parent_id = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                                  "code ='{id_form}' and rownum = 1".format(id_form=id_form)).fetchone()[0])

for protocol_name in sheets_names:
    code_form = int(connection.cursor().execute("SELECT MAX(TO_NUMBER(code)) + 1 FROM solution_form.form where"
                                                " trim(TRANSLATE(code, '0123456789-,.', ' ')) is null").fetchone()[0])
    add_form = "DECLARE rc pkg_global.ref_cursor_type;" \
               " BEGIN p_content.save_form(" \
               "NULL, NULL, {parent_id}, {id_form}," \
               " {id_form},  '{protocol_name}', ''," \
               " 0.0, 1, 1, 0," \
               " '', NULL, NULL, 0, 0, rc);COMMIT;END;".format(protocol_name=str(protocol_name),
                                                               id_form=code_form, parent_id=parent_id)
    create_form.execute(add_form)
    id = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                         "code = '{code_form}'"
                                         " and rownum = 1".format(code_form=code_form)).fetchone()[0])

    for item_name in protocol_rows:
        insert_form_item = """
        DECLARE rc pkg_global.ref_cursor_type;
        BEGIN
        p_content.save_form_item(
            NULL
            , NULL
            , '{id}'
            , NULL
            , NULL
            , '{code}'
            , {sortcode}
            , {type}
            , {type_value}
            , NULL
            , 0.0
            , '{item_name}'
            , NULL
            , 1
            , ''
            , 0
            , 0
            , {is_multi}
            , NULL
            , NULL
            , NULL
            , ''
            , ''
            , 0
            , 0
            , 0
            , ''
            , 0
            , NULL
            , ''
            , 0
            , NULL
            , rc);
            COMMIT;
            END;
            """.format(item_name=item_name[1],
                       id=id, code=protocol_rows.index(item_name),
                       sortcode=protocol_rows.index(item_name),
                       type=item_name[0],
                       type_value=item_name[2],
                       is_multi=item_name[3],
                       )
        create_form.execute(insert_form_item)
        if item_name[2] == 2:
            for answer in item_name[4]:
                get_if_form_item = int(connection.cursor().execute("SELECT SOLUTION_MED.PKG_GLOBAL.GET_NEXT_ID('SOLUTION_FORM',"
                                                               " 'FORM_ITEM') - 1 FROM DUAL").fetchone()[0])
                get_if_form_item_value = int(connection.cursor().execute("SELECT SOLUTION_MED.PKG_GLOBAL.GET_NEXT_ID('SOLUTION_FORM',"
                                                               " 'FORM_ITEM') FROM DUAL").fetchone()[0])
                insert_form_item_value = """
                INSERT INTO SOLUTION_FORM.FORM_ITEM_VALUE (
                ID
                ,FORM_ITEM_ID
                ,CODE
                ,SORTCODE
                ,TEXT
                ,NOTE
                ,BALL
                ,STATUS
                ,IS_DEFAULT
                ,NAME
                ,ROOT_ID
                ,IGNORE_TEXT
                ) VALUES (
                '{form_item_value}'
                ,'{form_item}'
                ,'1'
                ,1
                ,'{answer}'
                ,''
                ,NULL
                ,1
                ,0
                ,'{name_answer}'
                ,''
                ,NULL
                );
                COMMIT;
                """.format(form_item = get_if_form_item,form_item_value = get_if_form_item_value,
                           answer=answer, name_answer = answer)
                create_form.execute(insert_form_item_value)