# Lab 6: Code and Branch Coverage — Highway Toll Calculator

Line and branch coverage analysis of highway_toll.py (toll charges by axle count, peak hours and FASTag, plus monthly pass advice) using **coverage** and **pytest**. The original script and starter tests come from the assigned repo SETAPESU26/L6_L7_36_highway_toll.

## Results

Coverage of `highway_toll.py` (28 statements, 18 branches):

| Test file                            | Tests | Line coverage | Branch coverage | Missing          |
| ------------------------------------ | ----- | ------------- | --------------- | ---------------- |
| `test_highway_toll.py` (starter)     | 2     | 46%           | 39%             | 15 lines         |
| `CodeCoverageTest_highway_toll.py`   | 8     | 100%          | 96%             | `12->14`, `14->19` |
| `BranchCoverageTest_highway_toll.py` | 23    | 100%          | 100%            | none             |

## Line coverage vs branch coverage

`CodeCoverageTest_highway_toll.py` runs every line of `highway_toll.py`, so line coverage is 100%. Branch coverage is still only 96%, because two decisions were only ever taken one way:

- `12->14`: `if is_peak:` was never False. Every toll calculation ran during peak hours, so the off-peak price was never checked.
- `14->19`: `if has_fastag:` was never False. Every vehicle had a FASTag, so the undiscounted price was never checked.

A bug in either of those paths, such as charging the peak surcharge all the time, would not have been caught even with 100% line coverage.

`BranchCoverageTest_highway_toll.py` adds tests for the missing paths (off-peak with FASTag, peak without FASTag) and for edge cases:

- 3, 4 and 5+ axle base tolls
- zero axles
- the fire engine exemption
- an exempt vehicle with an invalid axle count, which returns 0 before the axle check
- a non-exempt vehicle with invalid axles
- pass advice with no trips and with mixed trips

## Running it

```bash
pip install coverage pytest

# line coverage
coverage run -m pytest CodeCoverageTest_highway_toll.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_highway_toll.py
coverage report -m
```

## Folder structure

```
Lab_6/
├── highway_toll.py                      # module under test (unchanged)
├── test_highway_toll.py                 # starter tests from the assigned repo
├── CodeCoverageTest_highway_toll.py     # tests for line coverage
├── BranchCoverageTest_highway_toll.py   # tests for branch coverage
├── README.md
└── screenshots/
    ├── code_coverage_line.png           # line coverage report (100%)
    ├── code_coverage_branch.png         # same tests with --branch (96%)
    └── branch_coverage.png              # branch coverage report (100%)
```

## Submission checklist

- [x] Code coverage analysis with terminal screenshots
- [x] Branch coverage analysis with terminal screenshots
- [x] `CodeCoverageTest_highway_toll.py` (at least 90% line coverage)
- [x] `BranchCoverageTest_highway_toll.py` (at least 90% branch coverage)
- [x] Commit history: one commit for the code coverage tests, one for the branch coverage tests
