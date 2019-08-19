from check_func import *
from except_func import print_exception

def parse_excel_workbook(wb):
    protocols = {}
    try:
        for ws in wb.worksheets:
            sheet_name = ''
            protocol_rows = []

            for i in range(1, 3):  # find name protocol in the first three excel_row
                if ws.cell(i, 1).value:
                    sheet_name = ws.cell(i, 1).value
                    break

            for excel_row in range(5, ws.max_row):  # 5 excel_row is begin protocol_row
                element_data = ws.cell(excel_row, 2).value
                type_element_data = check_type_element_data(str(element_data)) if element_data else False
                if element_data == None:
                    if ws.cell(excel_row, 5).value:
                        for i in check_answers(ws.cell(excel_row, 5).value):
                            protocol_rows[len(protocol_rows) - 1][4].append(i) # append row without header to higher row
                        continue
                    else:
                        continue

                element_data = char_decoder(str(ws.cell(excel_row, 2).value))


                element = check_element(ws.cell(excel_row, 1).value, ws.cell(excel_row, 5).value)
                # 0 - разделитель
                # 1 - редактируемый
                # 2 - невидимый
                # 3 - только
                # чтение
                # 4 - неактивный;
                type_answer = check_type_answer(ws.cell(excel_row, 3).value)
                # 0 - Простой текст (строка) 1 - Описание (много строк) 2 - Значения из списка
                # 3 - Значения из внешнего справочника 4 - Формула 5 - Таблица 6 - Значение из системного справочника
                # 7 - Формула SQL 8 - Поле для ввода диагноза 9 - Поле для ввода услуг 10 - Значение из дерева
                # 11 - Значение из списка отмеченное галочками 12 - Файл 13 - Схема (изображение);
                multi_choise = check_multi_choise(ws.cell(excel_row, 4).value)
                # 0 or 1
                answers = check_answers(ws.cell(excel_row, 5).value)
                # Нарушений легочной вентиляции не зарегистрировано
                # Проба с физической нагрузкой - положительная
                excel_row = [element, element_data, type_answer, multi_choise, answers, type_element_data]
                protocol_rows.append(is_conclusion(check_choise_is_not_null(excel_row)))
            protocols[sheet_name] = protocol_rows
    except Exception as e:
        print('Problem with parse Excel')
        print_exception(e)
    return protocols


def check_null_excel_sheet(protocols):
    for i in list(protocols):
        if len(protocols[i]) == 0:
            del protocols[i]
    return protocols