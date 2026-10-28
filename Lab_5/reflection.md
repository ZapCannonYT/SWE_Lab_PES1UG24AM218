# Lab 5 – Reflection

## 1. Which issues were easiest and which were hardest to fix, and why?

Easiest were the mechanical ones: the four Flake8 findings and the snake_case renames, because each message names the line and the fix is obvious. The hardest was B602 (shell=True). Deleting the flag is not enough: runScene still has to run a script, so I had to decide what input is legal (a bare file name inside scenes/), validate it, and pass an argv list. The mutable default argument was the trickiest to *notice* as a real bug: Pylint flags it as W0102, but only running the program showed the effect (a light with a temperature setting).

## 2. Did the tools report anything that was a false positive or not worth fixing?

B404 (importing subprocess) is informational: the import isn't the problem, how it's used is. I kept the import and added a justified `# nosec`, same for B603 on the call, after making the call shell-free and validated. B105 was a fair hit here (the password was literally in the file) even though it's a demo value. Pylint's missing-docstring and naming messages don't change behaviour, but they make the code consistent and searchable, so I fixed them rather than disabling them.

## 3. What did static analysis miss that you found another way?

Two bugs came from running and reading the code, not from the tools: set_temperature raised KeyError for an unknown device, and `main()` executed on import (side effects, hard to test). The shared-settings bug was flagged by Pylint only as a generic "dangerous default value", while its actual symptom showed up in the program output. Static analysis finds patterns, not intent, so it complements running the program and tests rather than replacing them.

## 4. How would you use these tools in a real workflow?

Run Flake8 and Pylint as pre-commit hooks and in CI so style and quality regressions fail the build, and Bandit in CI with a policy of failing on Medium/High. Suppressions (`# nosec`, `# pylint: disable`) should always carry a reason and be reviewed. Fix by severity: security first, then bugs, then style. Pin tool versions so a new release doesn't suddenly break builds. Tools catch the cheap problems early, which leaves code review for design and logic.
