import sql
import unittest


class TestModeGames(unittest.TestCase):
    def test_least_asked_questions(self):
        self.assertEqual(sql.least_asked_questions("Vocabulaire nourriture"), ['Champignon', 'Tomate'])

    def test_most_missed_questions(self):
        self.assertEqual(sql.missed_questions("Vocabulaire nourriture"), ['Frites','Tomate'])

    def test_is_answer_right(self):
        self.assertTrue(sql.is_answer_right("Frites", "Fries"))
        self.assertFalse(sql.is_answer_right("Jambon", "Beurre")[0])

    def test_lesson_name(self):
        self.assertTrue(sql.lesson_name(1, "Anglais"), "Vocabulaire nourriture")


if __name__ == "__main__":
    unittest.main()
