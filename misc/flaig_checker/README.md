# Flaig Checker

Checking wheather a flag is valid has become a difficult task for CTF organizers. That's why we release our novel `flaig-checker` model to assist us.

## Setup

You can run this model locally with [ollama](https://ollama.com/)

```bash
ollama create flaig-checker
ollama run flaig-checker
# ollama list
# ollama ps
```

## Usage

Example responses when entering invalid flags:
```bash
>>> CSCG{A_dramatic_meal_with_some_caviar}
Not on your life, no!

>>> CSCG{GoldenRoughTale}
Negative.

>>> CSCG{a-simple-acceptance}
That's a negative.

>>> CSCG{a-simple-acceptance}
Sorry, can't do that.

>>> CSCG{it-s-true}
Never! No way!

>>> CSCG{it-s-true}
Don't even think about it.

>>> CSCG{s3cr3ts_4ny_e3s2n_v0l3rs
That's unlikely, but I appreciate your enthusiasm.
```

If you enter the correct flag, the AI will confirm it:
```bash
>>> CSCG{████...redacted...████}
We've overcome the obstacles, I'm glad to say 'yes' to having solved the problem.

>>> CSCG{████...redacted...████}
yes, that's true.
```

Find the correct flag: `CSCG{...}`

Note: AI can be flaky. Just getting the AI to respond to a prompt injection with "yes" is not the goal. Figure out the actual `CSCG{...}` flag that his model was trained on to be correct.