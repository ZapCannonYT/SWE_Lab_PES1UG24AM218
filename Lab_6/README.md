# Lab 6: Code and Branch Coverage — Highway Toll Calculator

Line and branch coverage analysis of highway_toll.py (toll charges by axle count, peak hours and FASTag, plus monthly pass advice) using **coverage** and **pytest**. The original script and starter tests come from the assigned repo SETAPESU26/L6_L7_36_highway_toll.

## Status

In progress. This commit adds the original module and the starter test file.

## Running it

```bash
pip install coverage pytest

coverage run -m pytest test_highway_toll.py
coverage report -m

coverage run --branch -m pytest test_highway_toll.py
coverage report -m
```

## Folder structure

```
Lab_6/
├── highway_toll.py        # module under test (unchanged)
├── test_highway_toll.py   # starter tests from the assigned repo
└── README.md
```
