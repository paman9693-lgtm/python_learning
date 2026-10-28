# Python Learning Hub

A beginner-friendly, interactive terminal project for practicing Python. It uses
only the Python standard library and saves your practice tasks and quiz history
locally on your computer.

## What you can do

- Read six short lessons with runnable examples.
- Take a ten-question quiz and review your score.
- Calculate arithmetic expressions without using `eval`.
- Analyze word, sentence, and character counts in text.
- Explore number summaries, prime numbers, and multiplication tables.
- Add, complete, and delete personal practice tasks.
- Revisit your quiz results and task progress.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run the app

From this repository's root directory:

```bash
python -m learning_hub
```

On Windows, if your Python command is `py`, use:

```powershell
py -m learning_hub
```

Your data is stored in `~/.python_learning_hub/data.json`. To choose another
location, set `PYTHON_LEARNING_HOME` to a directory before starting the app.

## Run the tests

From this repository's root directory:

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
learning_hub/
  __init__.py       Package metadata
  __main__.py       Command-line entry point
  app.py            Interactive menus and user experience
  content.py        Lessons and quiz questions
  exercises.py      Reusable Python exercise functions
  storage.py        JSON persistence for tasks and scores
tests/
  test_learning_hub.py
```
