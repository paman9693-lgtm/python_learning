"""Terminal interface for the Python Learning Hub."""

from collections.abc import Callable

from .content import LESSONS, QUESTIONS, Lesson, Question
from .exercises import (
    ExerciseError,
    analyze_text,
    calculate,
    fibonacci_sequence,
    is_prime,
    multiplication_table,
    summarize_numbers,
)
from .storage import DataStore, StorageError


MENU = """
================================
       PYTHON LEARNING HUB
================================
1. Read a Python lesson
2. Take the Python quiz
3. Use the safe calculator
4. Analyze some text
5. Explore numbers
6. Manage practice tasks
7. View your learning progress
8. Generate a Fibonacci sequence
0. Exit
"""


def _pause(input_fn: Callable[[str], str]) -> None:
    input_fn("\nPress Enter to return to the menu...")


def show_lessons(input_fn: Callable[[str], str], print_fn: Callable[..., None]) -> None:
    print_fn("\n--- Python lessons ---")
    for index, lesson in enumerate(LESSONS, start=1):
        print_fn(f"{index}. {lesson.title}")
    print_fn("0. Back")
    choice = input_fn("Choose a lesson: ").strip()
    if choice == "0":
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(LESSONS):
        print_fn("Please choose one of the listed lesson numbers.")
        return
    lesson = LESSONS[int(choice) - 1]
    print_fn(f"\n{lesson.title}\n{'-' * len(lesson.title)}")
    print_fn(lesson.explanation)
    print_fn(f"\nExample:\n{lesson.example}")


def ask_question(
    question: Question,
    number: int,
    total: int,
    input_fn: Callable[[str], str],
    print_fn: Callable[..., None],
) -> bool:
    print_fn(f"\nQuestion {number}/{total}: {question.prompt}")
    for index, choice in enumerate(question.choices, start=1):
        print_fn(f"  {index}. {choice}")
    answer = input_fn("Your answer: ").strip()
    if answer.isdigit() and int(answer) - 1 == question.answer:
        print_fn("Correct!")
        return True
    print_fn(f"Not quite. {question.explanation}")
    return False


def take_quiz(
    store: DataStore,
    input_fn: Callable[[str], str],
    print_fn: Callable[..., None],
) -> None:
    score = sum(
        ask_question(question, index, len(QUESTIONS), input_fn, print_fn)
        for index, question in enumerate(QUESTIONS, start=1)
    )
    store.record_quiz_result(score, len(QUESTIONS))
    print_fn(f"\nYour score: {score}/{len(QUESTIONS)} ({round(score / len(QUESTIONS) * 100)}%)")
    if score == len(QUESTIONS):
        print_fn("Excellent work! You got every question right.")
    elif score >= len(QUESTIONS) * 0.7:
        print_fn("Great job. Review the lessons for anything you missed.")
    else:
        print_fn("Keep practicing. The lessons are here whenever you need them.")


def use_calculator(input_fn: Callable[[str], str], print_fn: Callable[..., None]) -> None:
    expression = input_fn("Enter an arithmetic expression: ")
    print_fn(f"Result: {calculate(expression)}")


def use_text_analyzer(input_fn: Callable[[str], str], print_fn: Callable[..., None]) -> None:
    print_fn("Enter a line of text (or leave it blank to cancel):")
    text = input_fn("> ")
    if not text:
        print_fn("No text entered.")
        return
    report = analyze_text(text)
    for label, key in (
        ("Characters", "characters"),
        ("Characters without spaces", "characters_without_spaces"),
        ("Words", "words"),
        ("Sentences", "sentences"),
        ("Unique words", "unique_words"),
    ):
        print_fn(f"{label}: {report[key]}")
    common = report["most_common_words"]
    print_fn(f"Most common words: {common or 'None'}")


def _read_number(prompt: str, input_fn: Callable[[str], str]) -> float:
    try:
        return float(input_fn(prompt).strip())
    except ValueError as error:
        raise ExerciseError("Please enter a valid number.") from error


def explore_numbers(input_fn: Callable[[str], str], print_fn: Callable[..., None]) -> None:
    try:
        values = input_fn("Enter numbers separated by commas: ")
        numbers = [float(value.strip()) for value in values.split(",") if value.strip()]
        summary = summarize_numbers(numbers)
        print_fn(
            "Count: {count} | Sum: {sum:g} | Min: {minimum:g} | "
            "Max: {maximum:g} | Average: {average:g} | Median: {median:g}".format(**summary)
        )
        whole_number = _read_number("Enter a whole number for a prime check: ", input_fn)
        if not whole_number.is_integer():
            raise ExerciseError("Prime checks need a whole number.")
        integer = int(whole_number)
        print_fn(f"{integer} is {'prime' if is_prime(integer) else 'not prime'}.")
        table_number = int(_read_number("Enter a number for its multiplication table: ", input_fn))
        for line in multiplication_table(table_number):
            print_fn(line)
    except (ValueError, ExerciseError) as error:
        print_fn(f"Input error: {error}")


def explore_fibonacci(input_fn: Callable[[str], str], print_fn: Callable[..., None]) -> None:
    try:
        count = int(input_fn("How many Fibonacci terms (1-50)? ").strip())
        sequence = fibonacci_sequence(count)
        print_fn("Fibonacci sequence: " + ", ".join(map(str, sequence)))
    except (ValueError, ExerciseError) as error:
        print_fn(f"Input error: {error}")


def manage_tasks(
    store: DataStore,
    input_fn: Callable[[str], str],
    print_fn: Callable[..., None],
) -> None:
    print_fn("\n--- Practice tasks ---")
    data = store.load()
    if not data["tasks"]:
        print_fn("You have no tasks yet.")
    for task in data["tasks"]:
        marker = "x" if task.get("done") else " "
        print_fn(f"[{marker}] {task.get('id', '?')} - {task.get('title', '(untitled)')}")
    print_fn("\na. Add a task   c. Complete a task   d. Delete a task   0. Back")
    choice = input_fn("Choose an action: ").strip().lower()
    if choice == "a":
        title = input_fn("Task description: ")
        task = store.add_task(title)
        print_fn(f"Added task {task['id']}.")
    elif choice == "c":
        task = store.complete_task(input_fn("Task id to complete: ").strip())
        print_fn(f"Completed: {task['title']}")
    elif choice == "d":
        store.delete_task(input_fn("Task id to delete: ").strip())
        print_fn("Task deleted.")
    elif choice != "0":
        print_fn("Unknown action.")


def show_progress(store: DataStore, print_fn: Callable[..., None]) -> None:
    data = store.load()
    completed = sum(bool(task.get("done")) for task in data["tasks"])
    print_fn("\n--- Your learning progress ---")
    print_fn(f"Lessons available: {len(LESSONS)}")
    print_fn(f"Practice tasks: {completed}/{len(data['tasks'])} completed")
    results = data["quiz_results"]
    if not results:
        print_fn("Quiz history: no quizzes taken yet.")
        return
    latest = results[-1]
    best = max(result.get("percentage", 0) for result in results)
    print_fn(f"Quizzes taken: {len(results)}")
    print_fn(f"Latest quiz: {latest['score']}/{latest['total']} ({latest['percentage']}%)")
    print_fn(f"Best quiz score: {best}%")


def main() -> None:
    store = DataStore()
    actions: dict[str, Callable[[], None]] = {
        "1": lambda: show_lessons(input, print),
        "2": lambda: take_quiz(store, input, print),
        "3": lambda: use_calculator(input, print),
        "4": lambda: use_text_analyzer(input, print),
        "5": lambda: explore_numbers(input, print),
        "6": lambda: manage_tasks(store, input, print),
        "7": lambda: show_progress(store, print),
        "8": lambda: explore_fibonacci(input, print),
    }
    print("Welcome! Learn a concept, try an exercise, and keep practicing.")
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Happy coding. See you next time!")
            return
        action = actions.get(choice)
        if action is None:
            print("Please enter a number from 0 to 8.")
            continue
        try:
            action()
        except (ExerciseError, StorageError, ValueError) as error:
            print(f"Could not complete that action: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        _pause(input)
