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


