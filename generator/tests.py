import unittest
from generator import main, sql_func, excel_func, check_func, except_func


class TestCheckFunc(unittest.TestCase):

    def test_check_element_(self):
        self.assertEqual(check_func.check_element('Заголовок', None), 0)
        self.assertEqual(check_func.check_element('Заголовок', ['value']), 1)
        self.assertEqual(check_func.check_element('Вопрос', ['value']), 1)
        self.assertEqual(check_func.check_element('неизвестный элемент', ['value']), 1)
        self.assertEqual(check_func.check_element(None, None), 1)

    def test_check_type_answer(self):
        self.assertEqual(check_func.check_type_answer('составной ответ'), 0)
        self.assertEqual(check_func.check_type_answer('простой текст'), 0)
        self.assertEqual(check_func.check_type_answer('значения из списка'), 2)
        self.assertEqual(check_func.check_type_answer(None), 0)
        self.assertEqual(check_func.check_type_answer(''), 0)

    def test_check_multi_choise(self):
        self.assertEqual(check_func.check_multi_choise('Да'), 1)
        self.assertEqual(check_func.check_multi_choise('+'), 1)
        self.assertEqual(check_func.check_multi_choise('Нет'), 0)
        self.assertEqual(check_func.check_multi_choise('-'), 0)
        self.assertEqual(check_func.check_multi_choise(None), 0)
        self.assertEqual(check_func.check_multi_choise(''), 0)


    def test_check_answers(self):
        self.assertEqual(check_func.check_answers(''), [''])
        self.assertEqual(check_func.check_answers(None), [''])
        self.assertEqual(len(check_func.check_answers("""
        обычная
деформирован засчёт перегиба в области тела
деформирован засчёт перегиба в области дна
деформирован засчёт перегиба в области шейки
при перемене положения тела расправляется
""")), 5)
        self.assertEqual(len(check_func.check_answers("""
        по возрасту                                                                     по индивидуальному графику                                         не вакцинирован                                                                    

        """)), 3)
        self.assertEqual(check_func.check_answers(None), [''])
        self.assertEqual(len(check_func.check_answers(""""консультация педиатра, консультация хирурга, УЗ контроль через, УЗ контроль в динамике"
""")), 4)


class TestExcelFunc(unittest.TestCase):
    def setUp(self):
        self.path = 'test_protocol.xlsx'
        self.wb = main.load_workbook(self.path)


    def test_parse_excel_workbook(self):
        self.assertIsInstance(excel_func.parse_excel_workbook(self.wb), dict)


    def test_check_null_excel_sheet(self):
        protocols = excel_func.parse_excel_workbook(self.wb)
        excel_func.check_null_excel_sheet(protocols)
        self.assertEqual(len(protocols), 3)


class TestSqlFunc(unittest.TestCase):

    def setUp(self):
        self.connection, self.sql_cursor = sql_func.connect_MED()
        self.table_FORM = 'solution_form.FORM'
        self.table_FORM_ITEM = 'solution_form.FORM_ITEM'
        self.table_FORM_ITEM_VALUE = 'solution_form.FORM_ITEM_VALUE'

    def test_connect_MED(self):
        self.assertGreater(int(self.connection.version.split('.')[0]), 11)

    def test_sql_get_all_protocol_folders(self):
        protocol_folder = sql_func.sql_get_all_protocol_folders(self.connection)
        self.assertIsInstance(protocol_folder, list)

    def test_sql_create_parent_form(self):
        sql_func.sql_create_parent_form(self.connection, 'Тестовая Папка')
        parent_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        self.assertEqual(self.get_name_by_id(self.sql_cursor, self.table_FORM, parent_id), 'Тестовая Папка')
        sql_func.del_by_id(self.sql_cursor, parent_id)

    def test_sql_create_children_form(self):
        sql_func.sql_create_parent_form(self.connection, 'Тестовая Папка')
        parent_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        sql_func.sql_create_children_form(self.connection, parent_id, 'Тестовый протокол')
        children_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        self.assertEqual(self.get_name_by_id(self.sql_cursor, self.table_FORM, children_id), 'Тестовый протокол')
        sql_func.del_by_id(self.sql_cursor, parent_id)

    def test_sql_insert_form_item(self):
        sql_func.sql_create_parent_form(self.connection, 'Тестовая Папка')
        parent_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        code = sql_func.sql_create_children_form(self.connection, parent_id, 'Тестовый протокол')
        id = sql_func.sql_get_id_by_code(code, self.connection)
        sql_func.sql_insert_form_item(self.sql_cursor, id, 1, [0, 'Тестова строка', 0, 0, [''], 0])
        row = self.get_sql_form_item_row(self.sql_cursor, id)
        self.assertEqual(row[0][15],  'Тестова строка')
        sql_func.del_by_id(self.sql_cursor, parent_id)

    def test_sql_insert_form_item_value(self):
        sql_func.sql_create_parent_form(self.connection, 'Тестовая Папка')
        parent_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        code = sql_func.sql_create_children_form(self.connection, parent_id, 'Тестовый протокол')
        id_children = sql_func.sql_get_id_by_code(code, self.connection)
        sql_func.sql_insert_form_item(self.sql_cursor, id_children, 1, [0, 'Тестова строка', 0, 0,
                                                                        ['Тестовый ответ 1', 'Тестовый ответ 2'], 0])
        id_form_item = sql_func.sql_get_id_form_item(self.sql_cursor)
        id_form_item_value = sql_func.sql_get_id_form_item_value(self.connection)
        sql_func.sql_insert_form_item_value('Тестовый ответ', self.sql_cursor,
                                            id_form_item, id_form_item_value, 1)
        rows = self.get_sql_form_item_value_row(self.sql_cursor, id_form_item)
        self.assertEqual(len(rows), 1)
        sql_func.del_by_id(self.sql_cursor, parent_id)



    def get_name_by_id(self, sql_cursor, table,  id):
        return sql_cursor.execute(f"SELECT TEXT FROM {table} where id = '{id}'").fetchone()[0]

    def get_sql_form_item_row(self, sql_cursor, id):
        return sql_cursor.execute(f"""
        SELECT t.*
      ,decode(NVL(t.color, 0)
             ,0, (SELECT color FROM solution_form.form WHERE id = t.form_id)
             ,t.color) AS form_color
      ,qg.text AS question_group_text
  FROM solution_form.form_item     t
      ,solution_med.question_group qg
 WHERE ('' IS NULL OR t.id = '')
   AND ('{id}' IS NULL OR t.form_id = '{id}')
   AND ('' IS NULL OR t.status = '')
   AND qg.keyid(+) = t.group_id
 ORDER BY t.sortcode
        """).fetchall()


    def get_sql_form_item_value_row(self, sql_cursor, id):
        return sql_cursor.execute(f"""
        SELECT fiv.*
      ,(SELECT s.keyid
          FROM srvdep                             s
              ,solution_form.form_item_value_link fivl
         WHERE fivl.link_id = s.keyid
           AND fiv.id = fivl.form_item_value_id) AS srvdepid
      ,(SELECT s.text
          FROM srvdep                             s
              ,solution_form.form_item_value_link fivl
         WHERE fivl.link_id = s.keyid
           AND fiv.id = fivl.form_item_value_id) AS srvdep
      ,(SELECT fivl.id
          FROM solution_form.form_item_value_link fivl
         WHERE fiv.id = fivl.form_item_value_id) AS value_link
  FROM solution_form.form_item_value fiv
 WHERE ('' IS NULL OR fiv.id = '')
   AND ('{id}' IS NULL OR fiv.form_item_id = '{id}')
   AND (NULL IS NULL OR fiv.text = NULL)
 ORDER BY fiv.sortcode
           """).fetchall()

#
class TestMain(unittest.TestCase):
    def setUp(self):
        self.connection, self.sql_cursor = sql_func.connect_MED()
        self.table_FORM = 'solution_form.FORM'
        self.path = 'test_protocol.xlsx'


    def test_create_protocol(self):
        sql_func.sql_create_parent_form(self.connection, 'Тестовая Папка')
        parent_id = sql_func.sql_get_last_id(self.connection, self.table_FORM)
        code = sql_func.sql_create_children_form(self.connection, parent_id, 'Тестовый протокол')
        exception = main.create_protocol(code, self.path)
        self.assertEqual(exception, 0)
        sql_func.del_by_id(self.sql_cursor, parent_id)


if __name__ == "__main__":
    unittest.main()