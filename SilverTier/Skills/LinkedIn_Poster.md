# Skill: LinkedIn Poster

## Description
Allows the agent to post updates to a LinkedIn profile using browser automation.

## Usage
1. Create a file in `Drafts/` with the prefix `LINKEDIN_`.
2. Format: The content of the file will be posted exactly as is.
3. The user must move the file to `Outbox/` to trigger the actual post.

## Configuration
Requires `LINKEDIN_USER` and `LINKEDIN_PASSWORD` in `.env`.
Uses Playwright for automation.
