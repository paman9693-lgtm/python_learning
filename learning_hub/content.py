"""Beginner lessons and quiz questions used by the learning hub."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    title: str
    explanation: str
    example: str


@dataclass(frozen=True)
class Question:
    prompt: str
    choices: tuple[str, ...]
    answer: int
    explanation: str


LESSONS = (
    Lesson(
        "Variables and data types",
        "Variables give names to values. Python commonly uses int, float, str, and bool.",
        'name = "Aman"\nage = 20\nis_learning = True\nprint(f"{name} is {age}")',
    ),
    Lesson(
        "Lists and loops",
        "A list stores an ordered collection. A for loop visits each item in order.",
        'fruits = ["apple", "mango", "orange"]\nfor fruit in fruits:\n    print(fruit)',
    ),
    Lesson(
        "Functions",
        "Functions package reusable work. Parameters provide input and return sends back a result.",
        "def rectangle_area(width, height):\n    return width * height\n\nprint(rectangle_area(4, 3))",
    ),
    Lesson(
        "Dictionaries",
        "A dictionary maps keys to values, making named data easy to find and update.",
        'student = {"name": "Aman", "score": 92}\nprint(student["name"])\nstudent["passed"] = True',
    ),
    Lesson(
        "Exceptions",
        "Exceptions describe errors. Handle only the expected error so other problems stay visible.",
        "try:\n    number = int(input('Enter a number: '))\nexcept ValueError:\n    print('That was not a whole number.')",
    ),
    Lesson(
        "Files and context managers",
        "The with statement closes a file reliably, even if an error happens while using it.",
        'from pathlib import Path\n\nPath("notes.txt").write_text("Hello!", encoding="utf-8")\ntext = Path("notes.txt").read_text(encoding="utf-8")',
    ),
)


QUESTIONS = (
    Question(
        "Which symbol starts a comment in Python?",
        ("//", "#", "--", "/*"),
        1,
        "A hash (#) starts a single-line Python comment.",
    ),
    Question(
        "What does len([3, 5, 7]) return?",
        ("2", "3", "15", "7"),
        1,
        "There are three items in the list.",
    ),
    Question(
        "Which keyword defines a function?",
        ("func", "function", "def", "make"),
        2,
        "Use def followed by the function name and parentheses.",
    ),
    Question(
        "What is the result of 9 // 2?",
        ("4", "4.5", "1", "18"),
        0,
        "The // operator performs floor division and returns 4.",
    ),
    Question(
        "Which collection stores unique values?",
        ("list", "tuple", "set", "dict values"),
        2,
        "A set contains distinct values.",
    ),
    Question(
        "What value does a function return if it has no return statement?",
        ("0", "False", "None", "An empty string"),
        2,
        "Python returns None when a function does not explicitly return a value.",
    ),
    Question(
        "Which mode adds text to the end of a file?",
        ("r", "w", "a", "x"),
        2,
        "The a (append) mode adds data after the existing content.",
    ),
    Question(
        "What does range(3) produce when used in a loop?",
        ("1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3"),
        1,
        "range(3) starts at zero and stops before three.",
    ),
    Question(
        "Which block handles an exception?",
        ("catch", "except", "error", "finally only"),
        1,
        "An except block handles matching exceptions raised in its try block.",
    ),
    Question(
        "What is the type of {'name': 'Aman'}?",
        ("list", "set", "tuple", "dict"),
        3,
        "Curly braces containing key-value pairs create a dictionary.",
    ),
)
