import responses
import json
import os
import unittest

from PittAPI import textbook

TERM = '1000'
SCRIPT_PATH = os.path.dirname(__file__)


class TextbookTest(unittest.TestCase):
    def setUp(self):
        self.validate_term = textbook._validate_term
        self.validate_course = textbook._validate_course
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses_CS.json')) as f:
            self.cs_data = json.load(f)
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses_STAT.json')) as f:
            self.stat_data = json.load(f)

    @unittest.skip
    def test_term_validation(self):
        if len(TERM) != 0:
            self.assertEqual(self.validate_term(TERM), TERM)

        self.assertEqual(self.validate_term('2000'), '2000')
        self.assertRaises(ValueError, self.validate_term, '1')
        self.assertRaises(ValueError, self.validate_term, 'a')

        self.assertRaises(ValueError, self.validate, '100')

    def test_validate_course_correct_input(self):
        self.assertEqual(self.validate_course('0000'), '0000')
        self.assertEqual(self.validate_course('0001'), '0001')
        self.assertEqual(self.validate_course('0012'), '0012')
        self.assertEqual(self.validate_course('0123'), '0123')
        self.assertEqual(self.validate_course('1234'), '1234')
        self.assertEqual(self.validate_course('9999'), '9999')

    def test_validate_course_improper_input(self):
        self.assertEqual(self.validate_course('0'), '0000')
        self.assertEqual(self.validate_course('1'), '0001')
        self.assertEqual(self.validate_course('12'), '0012')
        self.assertEqual(self.validate_course('123'), '0123')

    def test_validate_course_incorrect_input(self):
        self.assertRaises(ValueError, self.validate_course, '')
        self.assertRaises(ValueError, self.validate_course, '00000')
        self.assertRaises(ValueError, self.validate_course, '11111')
        self.assertRaises(ValueError, self.validate_course, 'hi')

    def test_construct_query(self):
        construct = textbook._construct_query
        course_query = 'compare/courses/?id=9999&term_id=1111'
        book_query = 'compare/books?id=9999'

        self.assertEqual(construct('courses', '9999', '1111'), course_query)
        self.assertEqual(construct('books', '9999'), book_query)

    def test_find_item(self):
        find = textbook._find_item('id', 'key', 'test')
        test_data = [
            {'id': 1, 'key': 1},
            {'id': 2, 'key': 4},
            {'id': 3, 'key': 9},
            {'id': 4, 'key': 16},
            {'id': 5, 'key': 25}
        ]

        for i in range(1, 6):
            self.assertEqual(find(test_data, i), i ** 2)

        self.assertRaises(LookupError, find, test_data, 6)

    @responses.activate
    def test_get_textbook(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        self.assertRaises(TypeError, textbook.get_textbook, '0000', 'CS', '401')

    @responses.activate
    def test_invalid_course_name(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '000', 'EXIST', None)

    @responses.activate
    def test_invalid_instructor(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '447', 'EXIST', None)

    @responses.activate
    def test_invalid_section(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '401', None, '9999')

    @responses.activate
    def test_get_textbook_no_section_or_instructor(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        self.assertRaises(TypeError, textbook.get_textbook, TERM, 'CS', '401', None, None)

    @responses.activate
    def test_textbook_get_textbook(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        instructor_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            instructor='GARRISON III'
        )

        section_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            section='1030'
        )
        self.assertIsInstance(instructor_test, list)
        self.assertIsInstance(section_test, list)

    @responses.activate
    def test_textbook_get_textbooks(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                      json=self.cs_data, status=201)
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22594&term_id=1000',
                      json=self.stat_data, status=201)
        multi_book_test = textbook.get_textbooks(
            term=TERM,
            courses=[
                {'department': 'CS', 'course': '445', 'section': '1030'},
                {'department': 'STAT', 'course': '1000', 'instructor': 'WANG'}])
        self.assertIsInstance(multi_book_test, list)

    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'TEST', '000', 'EXIST', None)
