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

## Reviewer
> database/reviewer.py

As mentioned before, we need to review links by hand.
Our problem is to keep track about which link was reviewed and which was not.

This script help us to review links opening them on browser and saving it
if it will be ignored or not. We can specify a parameter to tell how many
links will be reviewed. Then the files will be updated with unreviewed links
(if there is any one left) and ignored links.

## MsgGenerator
> notification/msg_generator.py

From a template, this tool generates a message text explaining how Passarama
works and the results obtained to a specific fansub.
