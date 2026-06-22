# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When the game first started there was a dark themed screen where there is a left sidebar with settings and more information. In the center of the screen there is the game title, a field to enter a quess, a debug info window, and other options at the bottom to restart the game and enter the guess. One concrete bug that I ran into was entering the guess using the enter key does not work as the field says. Another bug was that clicking new game does not seem to reset the score.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| New Game | Reset game score | Does not reset game score | None |
| Enter 1 after guessing 100 | Go higher | Go lower | None |
| Enter guess after resetting winning game | Go lower | You already won | None |

---

## 2. How did you use AI as a teammate?

- The AI tool that I used as a teammate for this project was Claude Code. 
- One example of an AI suggestion that was correct was turning both the guess number and secret number into integers before they are compared. I verified the result because the program before was comparing the two values lexicographically, causing wrong results in comparisons. After the changes, the comparisons now return the correct suggestion.
- One example of a misleading suggestion was suggesting to reset the number of attemts to 0 upon resetting the game. This suggestion is incorrect because when the player resets the game, they have made 0 attempts. I tested this using the developer debug info when entering my guesses.

---

## 3. Debugging and testing your fixes

- I decided whether a bug was really fixed by using both manual checks and pytest. During manual tests, I used multiple trials and seached for signals in the debug info that would hint at a persistent bug or incorrect result. For pytest, I had Claude Code generate tests that could be run to ensure that the program logic was working correctly.
- One test that I ran was to test the corrections Claude and I made to fix the higher and lower hints. To do this, I used manual tests to ensure that the correct hints were given no matter the target, guess, times reset, and using other factors. I also had Claude generate pytest tests to automatically check test cases for expected outputs.
- Claude Code helped me to design the tests to ensure that the correct hint was given depending on the guessed number and actual number. It helped to create a set of tests to compare a pair of guessed and expected numbers to see if the correct result would be returned.

---

## 4. What did you learn about Streamlit and state?

- Streamlit treats the script like one big function that reruns from top to bottom every time the user interacts with the page. Because every rerun starts fresh and wipes normal variables, st.session_state is used to carry values from one run to the next. This is why order matters and why certain bugs appeared in the program.

---

## 5. Looking ahead: your developer habits

- One habit that I want to want to keep from this project when prompting and being specific in my prompts. I used to use short prompts that were unspecific in instructions. During this project, I was able to use longer and clearer prompts while giving my AI assistant a role to increase efficiency.
- One thing that I want to do less is overly relying on the AI assistant to find the bugs that were causing the errors. I think that sometimes I was lazy in my approach and could have double checked AI's responses and edits before commiting to a change.
- This project changed the way that I thought about AI generated code because it opened my mind to the different ways of prompting the assistant to get a task done. However, it also showed me areas that AI might struggle in when attempting to solve a problem, or where it might be easier to do things manually.
