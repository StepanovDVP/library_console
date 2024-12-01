import os
import unittest
from unittest.mock import patch

from crud import author_crud, book_crud
from handlers import add_book, delete_book, search_book


class TestAddBookFunction(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые файлы после выполнения всех тестов."""
        cls._remove_test_files()

    @staticmethod
    def _remove_test_files():
        test_files = ['../infra/test_authors.json', '../infra/test_books.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    @patch('builtins.input', side_effect=['Book Test', 'Author Test', 'N', '2000'])
    @patch('builtins.print')
    def test_add_book(self, mock_print, mock_input):
        add_book()

        author_id = author_crud.get_author_id('Author Test')
        author_data = author_crud.get_author(author_id)
        self.assertEqual(author_data['full_name'], 'Author Test')
        self.assertIn(1, author_data['books'])

        book_data = book_crud.get_book_by_id(1)
        self.assertEqual(book_data['title'], 'Book Test')
        self.assertEqual(book_data['author'], [author_id])
        self.assertEqual(book_data['year'], '2000')
        self.assertEqual(book_data['status'], 'в наличии')

        self.assertIn(1, book_crud.data['index_by_title']['Book Test'])
        self.assertIn(1, book_crud.data['index_by_year']['2000'])
        self.assertEqual(author_crud.data['index_by_title']['Author Test'], 1)

        expected_message = 'Книга "Book Test" успешно добавлена с ID: 1'
        mock_print.assert_any_call(expected_message)

    @patch('builtins.input', side_effect=['Book Test1', 'Author Test', 'N', '2000'])
    @patch('builtins.print')
    def test_add_book_1(self, mock_print, mock_input):
        add_book()

        author_id = author_crud.get_author_id('Author Test')
        author_data = author_crud.get_author(author_id)
        self.assertEqual(author_data['full_name'], 'Author Test')
        self.assertIn(1, author_data['books'])

        book_data = book_crud.get_book_by_id(2)
        self.assertEqual(book_data['title'], 'Book Test1')
        self.assertEqual(book_data['author'], [author_id])
        self.assertEqual(book_data['year'], '2000')
        self.assertEqual(book_data['status'], 'в наличии')

        self.assertIn(2, book_crud.data['index_by_title']['Book Test1'])
        self.assertIn(2, book_crud.data['index_by_year']['2000'])
        self.assertEqual(author_crud.data['index_by_title']['Author Test'], 1)

        expected_message = 'Книга "Book Test1" успешно добавлена с ID: 2'
        mock_print.assert_any_call(expected_message)

    @patch('builtins.input', side_effect=['Book Test', 'Auth@r 1', 'N', '2001'])
    def test_add_book_invalid_author(self, mock_input, ):
        with self.assertRaises(ValueError):
            add_book()

    @patch('builtins.input', side_effect=['Book Test', 'Author Test', 'N', '2Oo1'])
    def test_add_book_invalid_year(self, mock_input, ):
        with self.assertRaises(ValueError):
            add_book()

    @patch('builtins.input', side_effect=['1', 'Book Test'])
    @patch('builtins.print')
    def test_search_book_by_title(self, mock_print, mock_input):
        search_book()
        expected_output = '''
        ID    Title                Authors                                            Year   Status
        ----------------------------------------------------------------------------------------------
        1     Book Test            Author Test                                        2000   в наличии
        '''.replace(' ', '').replace('\n', '')

        printed_output = ''.join(
            [call.args[0] for call in mock_print.call_args_list]
        ).replace(' ', '').replace('\n', '')

        self.assertEqual(
            hash(expected_output),
            hash(printed_output),
            'Распечатанная таблица не соответствует ожидаемому формату.'
        )

    @patch('builtins.input', side_effect=['2'])
    @patch('builtins.print')
    def test_delete_book(self, mock_print, mock_input):
        delete_book()
        expected_message = f'Книга с ID 2 успешно удалена!'
        mock_print.assert_any_call(expected_message)

        # Проверяем, что книга удалена
        self.assertNotIn(2, book_crud.data['elements'])
        self.assertNotIn(2, book_crud.data['index_by_title'].get('Test Book1', []))
        self.assertNotIn(2, book_crud.data['index_by_year'].get('2000', [1]))
        self.assertNotIn(2, author_crud.data['elements'][1]['books'])

    @patch('builtins.input', side_effect=['99'])
    def test_delete_book_not_found(self, mock_input):
        with self.assertRaises(LookupError) as context:
            delete_book()
        self.assertEqual(str(context.exception), 'Книга с ID 99 не найдена!')


if __name__ == '__main__':
    unittest.main()
