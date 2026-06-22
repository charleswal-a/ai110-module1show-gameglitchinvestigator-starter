# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- Glitchy Guesser is a number-guessing game where the player tries to find a randomly chosen secret number within a number of attempts. The difficulty settings control the number range and how many guesses are allowed, and the game tracks a running score and guess history. After each guess the hints show whether the guess was too high or too low until the player wins or runs out of attempts.
- Previously, "New Game" button only reset the attempts and secret, so the score carried over and a finished game stayed stuck, blocking new guesses. Additionally, the check_guess function had inverted high/low hints and compared the guess against the secret as strings, producing wrong directions..
- I rewrote the New Game handler to reset all five state values using the difficulty-aware range, which fixed both the score carrying over and stuck-game bugs. I corrected check_guess to turn both values to integers and return properly oriented hints. I also refactored it and the other logic functions into logic_utils.py.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Player chooses the normal difficulty.
2. PLayer enters a guess of 50.
3. Game returns "Go HIGHER!"
4. Player enters a guess or 75.
5. Game returns "Go HIGHER!"
6. Score and number of guesses updates after each guess.
7. Game ends after the correct guess or player runs out of guesses.


**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
