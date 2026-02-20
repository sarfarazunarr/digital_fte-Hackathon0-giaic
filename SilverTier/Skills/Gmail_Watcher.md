# Skill: Gmail Watcher

## Description
Automatically monitors a Gmail inbox for new, unread messages and imports them as tasks.

## Usage
1. Run `Watchers/gmail_watcher.py`.
2. New unread emails will appear in the `Inbox/` folder as `.md` files.
3. The Agent Loop will automatically pick these up for reasoning.

## Configuration
Requires `GMAIL_USER` and `GMAIL_APP_PASSWORD` (App Password) in `.env`.
Uses IMAP over SSL.
