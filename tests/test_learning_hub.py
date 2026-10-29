import json
import tempfile
import unittest
from pathlib import Path

from learning_hub.exercises import (
    ExerciseError,
    analyze_text,
    calculate,
    fibonacci_sequence,
    is_prime,
    multiplication_table,
    summarize_numbers,
)
from learning_hub.storage import DataStore, StorageError


class CalculatorTests(unittest.TestCase):
    def test_calculates_supported_expressions(self) -> None:
        self.assertEqual(calculate("2 + 3 * (4 - 1)"), 11)
        self.assertEqual(calculate("-7 // 2"), -4)
        self.assertEqual(calculate("2 ** 3"), 8)
        self.assertEqual(calculate("5 / 2"), 2.5)

    def test_rejects_code_and_oversized_exponents(self) -> None:
        for expression in ("__import__('os').system('echo unsafe')", "2 ** 9", "1 / 0"):
            with self.subTest(expression=expression):
                with self.assertRaises(ExerciseError):
                    calculate(expression)


class ExerciseTests(unittest.TestCase):
    def test_analyzes_text(self) -> None:
        report = analyze_text("Hello, hello! Python is fun.")
        self.assertEqual(report["words"], 5)
        self.assertEqual(report["unique_words"], 4)
        self.assertEqual(report["sentences"], 2)
        self.assertEqual(report["most_common_words"][0], ("hello", 2))

    def test_summarizes_odd_and_even_number_lists(self) -> None:
        self.assertEqual(summarize_numbers([1, 5, 3])["median"], 3)
        result = summarize_numbers([1, 4, 2, 3])
        self.assertEqual(result["median"], 2.5)
        self.assertEqual(result["average"], 2.5)

    def test_rejects_empty_number_list(self) -> None:
        with self.assertRaises(ExerciseError):
            summarize_numbers([])

    def test_prime_check_and_table(self) -> None:
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(97))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(21))
        self.assertEqual(multiplication_table(4, 3)[-1], "4 x 3 = 12")

    def test_generates_fibonacci_sequence(self) -> None:
        self.assertEqual(fibonacci_sequence(1), [0])
        self.assertEqual(fibonacci_sequence(8), [0, 1, 1, 2, 3, 5, 8, 13])
        self.assertEqual(len(fibonacci_sequence(50)), 50)

    def test_rejects_invalid_fibonacci_term_counts(self) -> None:
        for count in (0, 51, 2.5, True):
            with self.subTest(count=count):
                with self.assertRaises(ExerciseError):
                    fibonacci_sequence(count)


class DataStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary_directory.name) / "data.json"
        self.store = DataStore(self.path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_tasks_persist_and_can_be_completed_or_deleted(self) -> None:
        task = self.store.add_task("  Practice loops  ")
        self.assertEqual(task["title"], "Practice loops")
        self.assertFalse(self.store.load()["tasks"][0]["done"])

        completed = self.store.complete_task(task["id"])
        self.assertTrue(completed["done"])
        self.store.delete_task(task["id"])
        self.assertEqual(self.store.load()["tasks"], [])

    def test_records_quiz_history(self) -> None:
        self.store.record_quiz_result(8, 10)
        self.assertEqual(
            self.store.load()["quiz_results"],
            [{"score": 8, "total": 10, "percentage": 80}],
        )

    def test_reports_corrupt_json_instead_of_overwriting_it(self) -> None:
        self.path.write_text("{", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{")

    def test_rejects_empty_task_titles(self) -> None:
        with self.assertRaises(ValueError):
            self.store.add_task("  ")


if __name__ == "__main__":
    unittest.main()
