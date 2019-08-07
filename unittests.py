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
        self.assertEqual(check_func.check_type_answer('составной ответ'), 0)
        self.assertEqual(check_func.check_type_answer('значения из списка'), 2)
        self.assertEqual(check_func.check_type_answer(None), 0)
        self.assertEqual(check_func.check_type_answer(''), 0)




class TestExcelFunc(unittest.TestCase):
    pass

class TestSqlFunc(unittest.TestCase):
    pass

class TestMain(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()