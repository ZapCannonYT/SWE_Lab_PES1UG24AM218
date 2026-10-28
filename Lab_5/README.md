# Lab 5: Static Code Analysis — Smart Home Controller

Static analysis of smart_home.py (a smart home device controller) using **Pylint**, **Bandit** and **Flake8**, followed by fixing every reported issue. The original script comes from the assigned repo SETAPESU26/L5_36_smart_home.

## Results

| Tool   | Checks                                  | Before                  | After      |
| ------ | --------------------------------------- | ----------------------- | ---------- |
| Pylint | Code quality, naming, docstrings, logic | 4.80 / 10               | 10.00 / 10 |
| Bandit | Security                                | 1 High, 1 Medium, 2 Low | 0 issues   |
| Flake8 | PEP 8 style                             | 4 issues                | 0 issues   |

## What I changed

- **Security (Bandit):** removed shell=True from run_scene (command injection) and validate the script name; hub binds to 127.0.0.1 instead of 0.0.0.0; password is read from the HUB_PASSWORD environment variable instead of being hardcoded.
- **Bug found by running the program:** add_device(..., settings={}) used a mutable default, so all devices shared one settings dict and the light, fan and TV all showed a thermostat temperature. Each device now gets its own dict.
- **Quality (Pylint):** snake_case names, docstrings, consistent return values, 

  open(..., encoding="utf-8"), a `__main__` guard, and no crash on unknown device names.
- **Style (Flake8):** spacing, blank lines and line length.

Score after each fix: Pylint 4.80 → 10.00, then Bandit 4 → 0, then Flake8 4 → 0.

The full write-up is in [`REPORT.md`](REPORT.md); the issue table is in [`issues.md`](issues.md) and the reflection answers are in [`reflection.md`](reflection.md).

## Running it

```bash
python3 -m venv venv && source venv/bin/activate
pip install pylint bandit flake8

python smart_home.py

pylint smart_home.py > pylint_report.txt
bandit -r smart_home.py > bandit_report.txt
flake8 smart_home.py > flake8_report.txt
```

Optional environment variables: `HUB_HOST` (default `127.0.0.1`) and `HUB_PASSWORD`.

## Folder structure

```
Lab_5/
├── smart_home.py        # fixed source
├── REPORT.md            # lab report
├── issues.md            # issue table (what, where, how it was fixed)
├── reflection.md        # reflection answers
├── README.md
└── reports/
    ├── before/          # pylint / bandit / flake8 reports on the original file
    └── after/           # the same reports on the fixed file
```

## Submission checklist

- [x] Cleaned `smart_home.py` with all reported issues fixed
- [x] Lab report (`REPORT.md`)
- [x] Issue table (`issues.md`)
- [x] Reflection answers (`reflection.md`)
- [x] Before and after `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`
- [x] Commit history: initial version with errors, then one fix commit each for Pylint, Bandit and Flake8
