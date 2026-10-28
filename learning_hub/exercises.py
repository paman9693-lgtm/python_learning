"""Reusable, testable functions for the hub's hands-on exercises."""

import ast
import operator
import re
from collections import Counter


class ExerciseError(ValueError):
    """Raised when an exercise receives unsupported or invalid input."""


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate_node(node: ast.AST) -> int | float:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 8:
            raise ExerciseError("Exponents must be between -8 and 8.")
        if isinstance(node.op, (ast.Mult, ast.Pow)) and abs(left) > 1_000_000:
            raise ExerciseError("That calculation is too large.")
        result = _BINARY_OPERATORS[type(node.op)](left, right)
        if abs(result) > 1_000_000_000_000:
            raise ExerciseError("That calculation is too large.")
        return result
    raise ExerciseError("Use numbers and +, -, *, /, //, %, **, and parentheses only.")


def calculate(expression: str) -> int | float:
    """Evaluate basic arithmetic without executing arbitrary Python code."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_node(tree.body)
    except (SyntaxError, ZeroDivisionError, OverflowError) as error:
        raise ExerciseError(f"Invalid calculation: {error}") from error
    if isinstance(result, float) and not result.is_integer():
        return round(result, 10)
    if isinstance(result, float):
        return int(result)
    return result


def analyze_text(text: str) -> dict[str, object]:
    """Return useful counts and the most common words in a piece of text."""
    words = re.findall(r"\b[\w']+\b", text.casefold())
    counts = Counter(words)
    return {
        "characters": len(text),
        "characters_without_spaces": sum(not character.isspace() for character in text),
        "words": len(words),
        "sentences": sum(text.count(mark) for mark in ".!?"),
        "unique_words": len(counts),
        "most_common_words": counts.most_common(5),
    }


def summarize_numbers(numbers: list[float]) -> dict[str, float | int]:
    """Summarize a non-empty list of numeric values."""
    if not numbers:
        raise ExerciseError("Enter at least one number.")
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) / 2
    )
    return {
        "count": len(ordered),
        "sum": sum(ordered),
        "minimum": ordered[0],
        "maximum": ordered[-1],
        "average": sum(ordered) / len(ordered),
        "median": median,
    }


def is_prime(number: int) -> bool:
    """Return whether a whole number is prime."""
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def multiplication_table(number: int, limit: int = 10) -> list[str]:
    """Build a formatted multiplication table."""
    if limit < 1:
        raise ExerciseError("The table length must be at least one.")
    return [f"{number} x {index} = {number * index}" for index in range(1, limit + 1)]
