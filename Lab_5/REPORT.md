# Lab 5 Report: Static Code Analysis

|                   |                                                  |
| ----------------- | ------------------------------------------------ |
| **Name**          | Rahul Saran Sharma                               |
| **SRN**           | PES1UG24AM218                                    |
| **Class**         | AIML-D                                           |
| **Date**          | 28/10/2026                                       |
| **File analysed** | smart_home.py (repo SETAPESU26/L5_36_smart_home) |

## 1. Objective

Use **Pylint**, **Bandit** and **Flake8** to find quality, security and style problems in an assigned Python program, fix them, and confirm the fixes by rerunning the tools.

## 2. Program

smart_home.py is a smart home device controller. It registers devices in rooms, toggles them on and off, sets a thermostat within a safe range (16–30), lists devices by room, reports power use, and saves the state to home_state.json.

Running the original program showed one bug no tool named directly: every device, including the light and TV, reported a temperature setting, because all devices shared a single default settings dict.

## 3. Setup and commands

```bash
python3 -m venv venv && source venv/bin/activate
pip install pylint bandit flake8

pylint smart_home.py > pylint_report.txt
bandit -r smart_home.py > bandit_report.txt
flake8 smart_home.py > flake8_report.txt
```

Reports are stored in `reports/before/` (original file) and `reports/after/` (fixed file).

## 4. Results

| Stage              | Pylint     | Bandit                  | Flake8   |
| ------------------ | ---------- | ----------------------- | -------- |
| Original           | 4.80 / 10  | 1 High, 1 Medium, 2 Low | 4 issues |
| After Pylint fixes | 10.00 / 10 | 1 High, 1 Medium, 2 Low | 4 issues |
| After Bandit fixes | 10.00 / 10 | **0 issues**            | 4 issues |
| After Flake8 fixes | 10.00 / 10 | 0 issues                | 0 issues |

## 5. Issues found and how they were fixed

| Issue                                     | Type              | Line(s)  | Description                                                                                                                                                                                              | Fix Approach                                                                                                                                       |
| ----------------------------------------- | ----------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| B602 subprocess with shell=True           | Security (High)   | 51       | "bash scenes/" + sceneScript is run through a shell, so a name like `x; rm -rf ~` executes arbitrary commands (command injection, CWE-78).                                                               | Removed shell=True; call ["/bin/bash", path] as an argv list; accept only a bare file name that exists in scenes/, else ValueError.                |
| B104 Bind to all interfaces               | Security (Medium) | 4        | HUB_HOST = "0.0.0.0" exposes the hub on every network interface.                                                                                                                                         | Default to 127.0.0.1; allow an explicit override with the HUB_HOST env var.                                                                        |
| B105 Hardcoded password                   | Security (Low)    | 7        | HUB_PASSWORD = "smarthome-demo" is committed to source control.                                                                                                                                          | Read from the HUB_PASSWORD environment variable (empty default).                                                                                   |
| B404 subprocess import                    | Security (Low)    | 2        | Informational flag on importing subprocess.                                                                                                                                                              | Kept (needed by run_scene); # nosec B404 with reason, since the call is shell-free and validated. The B603 on the call is suppressed the same way. |
| Mutable default argument (W0102)          | Bug               | 11       | settings={} is created once and shared by **every** device. Setting the thermostat's temperature made the light, fan and TV all report temperature: 30 (visible in the demo output and home_state.json). | Default to None; create a new {} inside add_device. Light now prints {}; only the thermostat has temperature.                                      |
| Inconsistent returns (R1710)              | Bug / Quality     | 16–20    | toggleDevice returns a bool when found but falls off the end (implicit None) when not.                                                                                                                   | Early-return guard; explicit return None for the unknown-device case.                                                                              |
| Unknown device crashes (not tool-flagged) | Bug               | 24       | setTemperature("Unknown", x) raised KeyError (devices[deviceName]).                                                                                                                                      | Use devices.get(); print "Device not found" and return False.                                                                                      |
| `open()` without encoding (W1514)         | Quality           | 41       | Encoding depends on the platform locale, so the saved JSON can differ across machines.                                                                                                                   | open(file_name, "w", encoding="utf-8").                                                                                                            |
| Naming (C0103 ×16)                        | Style             | 11–49    | camelCase function/argument names violate PEP 8 snake_case.                                                                                                                                              | Renamed all (addDevice → add_device, deviceName → device_name, …) and every call site.                                                             |
| Missing docstrings (C0114, C0116 ×9)      | Style             | 1, 11–54 | No module or function docstrings.                                                                                                                                                                        | Added concise docstrings.                                                                                                                          |
| No `__main__` guard (not tool-flagged)    | Quality           | 72       | main() ran on import, writing home_state.json as a side effect.                                                                                                                                          | `if __name__ == "__main__": main()`.                                                                                                               |
| Magic numbers                             | Quality           | 28       | Safe range 16/30 hardcoded inline.                                                                                                                                                                       | MIN_TEMP/ MAX_TEMP constants.                                                                                                                      |
| E203 whitespace before :                  | Style (Flake8)    | 6        | "light" : 10.                                                                                                                                                                                            | Removed the space.                                                                                                                                 |
| E302 blank lines                          | Style (Flake8)    | 40       | One blank line before saveState, two required.                                                                                                                                                           | Added a blank line.                                                                                                                                |
| E261 inline comment spacing               | Style (Flake8)    | 66       | )# for app setup needs two spaces.                                                                                                                                                                       | Two spaces before #.                                                                                                                               |
| E501 line too long                        | Style (Flake8)    | 68       | 80 > 79 chars in the "Devices on" print.                                                                                                                                                                 | Wrapped the call over two lines.                                                                                                                   |

Not changed on purpose: the demo still calls toggle_device("Garage Door") and set_temperature("Ceiling Light", 20). Those are deliberate error-path demonstrations and now print clean messages.

## 6. Verification

After the final commit all three tools were rerun on the fixed file: Pylint 10.00/10, Bandit "No issues identified", Flake8 no output. The demo output now shows Light settings: {}, and only the thermostat has a temperature in home_state.json. Two Bandit Low findings (B404 on the subprocess import and B603 on the call) are suppressed with `# nosec` and a stated reason, because the call is shell-free and its argument is validated.

## 7. Reflection

### 1. Which issues were easiest and which were hardest to fix, and why?

Easiest were the mechanical ones: the four Flake8 findings and the snake_case renames, because each message names the line and the fix is obvious. The hardest was B602 (shell=True). Deleting the flag is not enough: runScene still has to run a script, so I had to decide what input is legal (a bare file name inside scenes/), validate it, and pass an argv list. The mutable default argument was the trickiest to *notice* as a real bug: Pylint flags it as W0102, but only running the program showed the effect (a light with a temperature setting).

### 2. Did the tools report anything that was a false positive or not worth fixing?

B404 (importing subprocess) is informational: the import isn't the problem, how it's used is. I kept the import and added a justified `# nosec`, same for B603 on the call, after making the call shell-free and validated. B105 was a fair hit here (the password was literally in the file) even though it's a demo value. Pylint's missing-docstring and naming messages don't change behaviour, but they make the code consistent and searchable, so I fixed them rather than disabling them.

### 3. What did static analysis miss that you found another way?

Two bugs came from running and reading the code, not from the tools: set_temperature raised KeyError for an unknown device, and main() executed on import (side effects, hard to test). The shared-settings bug was flagged by Pylint only as a generic "dangerous default value", while its actual symptom showed up in the program output. Static analysis finds patterns, not intent, so it complements running the program and tests rather than replacing them.

### 4. How would you use these tools in a real workflow?

Run Flake8 and Pylint as pre-commit hooks and in CI so style and quality regressions fail the build, and Bandit in CI with a policy of failing on Medium/High. Suppressions (`# nosec`, `# pylint: disable`) should always carry a reason and be reviewed. Fix by severity: security first, then bugs, then style. Pin tool versions so a new release doesn't suddenly break builds. Tools catch the cheap problems early, which leaves code review for design and logic.

## 8. Conclusion

Static analysis took the file from 4.80 to 10.00 on Pylint, removed every security finding including a command-injection risk, and made it PEP 8 clean. Running the program alongside the tools also exposed a real shared-state bug that the tools only hinted at, so the two approaches work best together.
