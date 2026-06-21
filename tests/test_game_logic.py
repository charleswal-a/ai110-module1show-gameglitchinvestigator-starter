"""
Regression tests for the bugs fixed in logic_utils.check_guess.

check_guess(guess, secret) returns a tuple: (outcome, message)
  outcome in {"Win", "Too High", "Too Low"}
"""

import pytest

from logic_utils import check_guess


# --- Win case -------------------------------------------------------------

def test_correct_guess_wins():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# --- High/Low DIRECTION bug ----------------------------------------------
# The original code returned inverted hints: a too-high guess told the
# player to "Go HIGHER" and a too-low guess to "Go LOWER". These assert the
# outcome AND that the hint points the player the correct way.

def test_too_high_guess_is_labeled_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_too_high_guess_tells_player_to_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_too_low_guess_is_labeled_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_low_guess_tells_player_to_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


# --- String-secret comparison bug ----------------------------------------
# app.py passes the secret as a STRING on even attempts. The old code fell
# back to lexicographic string comparison, where e.g. "9" > "100" is True,
# producing the wrong direction. The fix coerces both sides to int.

def test_string_secret_exact_match_still_wins():
    outcome, _ = check_guess(42, "42")
    assert outcome == "Win"


def test_string_secret_compares_numerically_not_lexicographically():
    # 9 < 100 numerically, but "9" > "100" lexicographically.
    # The buggy version would report "Too High"; correct is "Too Low".
    outcome, message = check_guess(9, "100")
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_string_secret_too_high_direction():
    # 50 > 20 numerically, but "50" > "20" lexicographically too — this
    # guards the happy path of the coercion still being correct.
    outcome, message = check_guess(50, "20")
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


@pytest.mark.parametrize(
    "guess, secret, expected",
    [
        (9, "100", "Too Low"),    # lexicographic trap
        (90, "100", "Too Low"),   # "90" > "100" lexicographically
        (100, "100", "Win"),
        (101, "100", "Too High"),
    ],
)
def test_string_secret_table(guess, secret, expected):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected
