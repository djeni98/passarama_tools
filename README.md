# Passarama Tools

This repository keeps tools related to https://github.com/djeni98/passarama.

## CleanDB
> database/clean_DB.py

This tool helps to clean dorama table. It interacts with 2 database files:

- `test-dev.sqlite`: The most recent database version created by crawler
- `old.sqlite`: The previous database version

Since we need to review link by link due to visual needs,
this tool is split in two sections:

- **initial**: Where it compares the old database with the new one to get
 unreviewed links and store them at a file.
- **final**: That drops ignored links from a file and update old
 database with the new one.

The reviewing part, between initial and final sections, have to be made by hand.
