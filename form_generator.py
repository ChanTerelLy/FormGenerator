import cx_Oracle
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import re

# primary data
table_path = input('Input table path:')
#table_path = "C:\\Users\Roman\OneDrive - Северный Арктический Федеральный Университет\MED\ДКМЦ\Протоколы\ДИАГНОСТИКА\функционалисты\Исследование функции внешнего дыхания.xlsx"
id_form = input('Input code parent form:')
file_name = os.path.splitext(os.path.basename(table_path))[0]
'''
input example 
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
        param_data = ws.cell(row, 1).value
        question_data = ws.cell(row, 2).value
        type_answer = ws.cell(row, 3).value
        multi_choise = ws.cell(row, 4).value
        answers = ws.cell(row, 5).value
        if ws.cell(row, 5).value:
            answers = ws.cell(row, 5).value.split('\n')
        elif ws.cell(row, 5).value == None:
            answers = ''
        if param_data == 'Заголовок':
            param_data = 0
        elif param_data == 'Вопрос':
            param_data = 1
        elif param_data == None:
            break
        if question_data == None:
            question_data = ''
        if type_answer == 'свободный ответ':
            type_answer = 0
        elif type_answer == 'значения из списка':
            type_answer = 2
        elif type_answer == None and param_data == 0:
            type_answer = ''
        if multi_choise:
            if multi_choise == re.match(r'^.ет', multi_choise):
                multi_choise = 0
            else:
                multi_choise = 1
        elif multi_choise == None:
            multi_choise = 0
        else:
            multi_choise = 0

        row = [param_data, question_data, type_answer, multi_choise, answers]
        protocol_rows.append(row)
    #print(protocol_rows)

# operation with oracle database
protocol_forms = []
connection = cx_Oracle.connect('solution_med/elsoft@med')
print(connection.version)
create_form = connection.cursor()
get_id_parent = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                                  "code ='{id_form}' and rownum = 1".format(id_form=id_form)).fetchone()[0])

for protocol_name in sheets_names:
    code_form = int(connection.cursor().execute("SELECT MAX(TO_NUMBER(code)) + 1 FROM solution_form.form where trim(TRANSLATE(code, '0123456789-,.', ' ')) is null").fetchone()[0])
    add_form = "DECLARE rc pkg_global.ref_cursor_type; BEGIN p_content.save_form(NULL, NULL, {rootid_form}, {id_form}, {id_form},  '{protocol_name}', '', 0.0, 1, 1, 0, '', NULL, NULL, 0, 0, rc);COMMIT;END;".format(protocol_name=str(protocol_name), id_form=code_form, rootid_form=get_id_parent)
    protocol_forms.append(add_form)
    create_form.execute(add_form)

    '''
    p_content.save_form ATTRIBUTES
                      p_form_id              IN solution_form.form.id%TYPE
                     ,p_form_connector_id    IN solution_form.form.form_connector_id%TYPE
                     ,p_root_id              IN solution_form.form.root_id%TYPE
                     ,p_code                 IN solution_form.form.code%TYPE
                     ,p_sortcode             IN solution_form.form.sortcode%TYPE
                     ,p_text                 IN solution_form.form.text%TYPE
                     ,p_note                 IN solution_form.form.note%TYPE
                     ,p_color                IN solution_form.form.color%TYPE
                     ,p_status               IN solution_form.form.status%TYPE
                     ,p_next_status          IN solution_form.form.next_status%TYPE
                     ,p_print_status         IN solution_form.form.print_status%TYPE
                     ,p_report_list_id       IN solution_form.form.report_list_id%TYPE
                     ,p_hide_status          IN solution_form.form.hide_status%TYPE
                     ,p_profile_typ_id       IN solution_form.form.profile_typ_id%TYPE
                     ,p_fill_form_type       IN solution_form.form.fill_form_type%TYPE
                     ,p_only_permitted_users IN solution_form.form.only_permitted_users%TYPE
                     ,p_rc                   IN OUT pkg_global.ref_cursor_type) AS'''
print(protocol_forms)
insert_form_item = "Declare" \
                   "rc pkg_global.ref_cursor_type;" \
                   "begin" \
                   "CALL p_content.save_form_item( NULL, NULL, '647750', NULL, NULL, '1', 1, 1, 1, NULL, 0.0," \
                   " 'вопрос1'" \
                   ", NULL, 1, '', 0, 1, 0, NULL, NULL, NULL, '', '', 0, 0, 0, '', 0, NULL, '', 0, NULL, ?)"
#create_form.execute(querystring)
#create_form.execute()
#print(connection.version)
