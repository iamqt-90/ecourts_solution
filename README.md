# eCourts Scraper

A Python utility to fetch court listings from the eCourts platform.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Submission Guidelines](#submission-guidelines)
- [Evaluation Criteria](#evaluation-criteria)

---

## Overview

This project automates the extraction of court listings from eCourts, based on user-supplied case details. The tool fetches information for specific days, retrieves serial numbers and court names, and downloads case documents or full cause lists where available[file:1].

---

## Features

- Accepts input via CNR or (Case Type, Number, Year)[file:1]
- Checks if a case is listed today or tomorrow[file:1]
- Retrieves serial number and court name if listed[file:1]
- Optionally downloads case PDF if available[file:1]
- Downloads the entire day's cause list on request[file:1]
- Outputs data to the console and saves results/cause list as JSON or text[file:1]
- CLI flags: `--today`, `--tomorrow`, `--causelist`
- *Bonus*: Simple web API interface (optional)[file:1]

---

## Requirements

- Python (ensure the correct version compatible with dependencies)[file:1]
- Internet connection to access public eCourts data[file:1]

---

## Installation

1. Clone this repository or unzip the given archive.
2. Set up your Python environment and install the required dependencies.
3. git clone <repository_url>
4. cd ecourts-scraper
5. pip install -r requirements.txt


---

## Usage

Provide case details as prompted or use CLI flags:
- `--today`: Check for today's listings
- `--tomorrow`: Check for tomorrow's listings
- `--causelist`: Download full cause list

Results are shown in the console and saved as JSON/text files[file:1].

---

## Output

- Console summary of case status, serial number, and court name[file:1]
- Results and cause list saved in JSON or text formats[file:1]

---

## Submission Guidelines

Submit your work through a public GitHub repo or as a ZIP file, including this README[file:1].

---

## Evaluation Criteria

- Accuracy & completeness of features
- Code quality & clarity
- Proper error handling, including for invalid input or network errors[file:1]

---



