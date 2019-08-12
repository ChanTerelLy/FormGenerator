import unittest
import main
import check_func
import excel_func
import sql_func

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
    pass

class TestMain(unittest.TestCase):
    def setUp(self):
        self.connection, self.sql_cursor = sql_func.connect_MED()

    def test_connect_MED(self):
        self.assertGreater(int(self.connection.version.split('.')[0]), 11)

    def test_sql_get_all_protocol_folders(self):
        #self.assertIsInstance(sql_func.sql_get_all_protocol_folders(self.connection))
        pass

if __name__ == "__main__":
    unittest.main()