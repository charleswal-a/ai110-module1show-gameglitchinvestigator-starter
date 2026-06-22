import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def proximity(guess, secret, low, high):
    """
    Return (emoji, label, color) describing how close a guess is.

    Pure presentation helper — does NOT affect game logic or scoring.
    `color` is a Streamlit markdown color name.
    """
    span = max(high - low, 1)
    ratio = abs(int(guess) - int(secret)) / span
    if ratio == 0:
        return "🎯", "Bullseye!", "green"
    if ratio <= 0.05:
        return "🔥", "Boiling hot", "red"
    if ratio <= 0.12:
        return "♨️", "Hot", "orange"
    if ratio <= 0.25:
        return "🌤️", "Warm", "orange"
    if ratio <= 0.45:
        return "❄️", "Cold", "blue"
    return "🧊", "Freezing", "blue"


def render_summary():
    """Render a summary table of the current session's guesses."""
    rounds = st.session_state.get("rounds", [])
    if not rounds:
        return
    with st.expander("📋 Session summary", expanded=True):
        st.table(rounds)
        st.caption(
            f"Guesses: {len(rounds)}  •  "
            f"Score: {st.session_state.score}  •  "
            f"Status: {st.session_state.status}"
        )


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "rounds" not in st.session_state:
    st.session_state.rounds = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: Fixed reset game logic using agent mode
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.rounds = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_summary()
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        emoji, label, color = proximity(
            guess_int, st.session_state.secret, low, high
        )

        # Color-coded Hot/Cold feedback (always shown — pure presentation).
        st.markdown(f"### {emoji} :{color}[{label}]")
        if show_hint and outcome != "Win":
            st.markdown(f":{color}[{message}]")

        # Record this round for the session summary table.
        st.session_state.rounds.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Result": outcome,
                "Proximity": f"{emoji} {label}",
            }
        )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_summary()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
