# Study Coach 🎓

Spaced-repetition flashcard harness (SM-2) + 3Blue1Brown-style animated explainer
videos, driven by [Hermes Agent](https://hermes-agent.nousresearch.com/docs).

Ask your agent: *"explain backprop like 3b1b"* → it scripts a
[Manim](https://www.manim.community/) scene and posts the video. Cards you flunk
get flagged for a video. A daily cron quizzes you on whatever the forgetting
curve says is due.

## Harness

```bash
python3 coach.py add "ML" "What does the gradient point toward?" "Steepest ascent"
python3 coach.py due --limit 5        # cards due now
python3 coach.py grade 3 4            # grade card #3 (0=blank .. 5=perfect)
python3 coach.py stats                # workload + 7-day forecast
python3 coach.py mine notes.md        # parse "Topic:: question :: answer" lines
```

Scheduling is textbook SM-2: grade < 3 resets the streak, ease adapts per card,
intervals grow geometrically. Cards live in `cards.json` (gitignored — your
study data stays yours; see `cards.example.json` for the schema).

## Explainer videos

`scenes/grad_descent.py` is a worked example — an 18s gradient-descent explainer
(loss curve, ball walking the gradient, update-rule reveal). Render:

```bash
manim -qm scenes/grad_descent.py GradDescentPoc
```

### Rootless manim setup (no sudo)

`pip install manim` fails on recent Ubuntu (pycairo/manimpango have no wheels).
Use conda-forge via micromamba instead:

```bash
mkdir -p ~/.local/micromamba
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
  | tar -xvj -C ~/.local/micromamba --strip-components=1 bin/micromamba
export MAMBA_ROOT_PREFIX=$HOME/.local/mamba
~/.local/micromamba/micromamba create -y -p $MAMBA_ROOT_PREFIX/envs/manim \
  -c conda-forge manim
export PATH=$MAMBA_ROOT_PREFIX/envs/manim/bin:$PATH
manim --version   # Manim Community v0.22.1
```

No LaTeX? Use `Text(..., font="DejaVu Sans Mono")` instead of `MathTex` —
works fine for most explainers.

## Agent integration

The repo is designed to be operated by an agent: a daily cron runs `coach.py due`,
posts question fronts (never answers) to chat, and grades your replies back into
the scheduler. See `coach.py` — it's stdlib-only, so any agent with a shell can
drive it.

## License

MIT — see LICENSE.
