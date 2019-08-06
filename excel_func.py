from check_gramma_func import check_type_element_data, check_answers, check_element, check_type_answer, \
    check_multi_choise


def parse_excel_workbook(protocols, wb):
    for ws in wb.worksheets:
        sheet_name = ''
        for i in range(1, 3):  # check name protocol in the first three excel_row
            if ws.cell(i, 1).value:
                sheet_name = ws.cell(i, 1).value
                break
        protocol_rows = []
        for excel_row in range(5, ws.max_row):  # 5 excel_row is begin protocol_row
            element_data = ws.cell(excel_row, 2).value
            type_element_data = check_type_element_data(element_data) if element_data else False
            if element_data == None:
                if ws.cell(excel_row, 5).value:
                    for i in check_answers(ws.cell(excel_row, 5).value):
                        protocol_rows[len(protocol_rows) - 1][4].append(i)
                    continue
                else:
                    continue

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
            protocol_rows.append(excel_row)
        protocols[sheet_name] = protocol_rows


def check_null_excel_sheet(protocols):
    for i in list(protocols):
        if len(protocols[i]) == 0:
            del protocols[i]