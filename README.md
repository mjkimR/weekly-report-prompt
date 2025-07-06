# Weekly Report Prompt Generator

This tool generates structured prompts for LLM to create weekly development reports based on Git commit data.

## Purpose

This project doesn't generate the actual weekly reports directly. Instead, it:
1. Collects Git commit data from specified repositories
2. Processes and structures the data
3. Generates a comprehensive prompt for LLM (Large Language Model)
4. Creates a template file that can be used with the LLM to generate the actual weekly report

## Features

- Collects commit data from multiple Git repositories
- Tracks changes since the last report
- Generates structured prompts for LLM consumption
- Maintains report history
- Configurable templates and settings

## Usage

1. Configure your repositories and settings in `config/config.yaml`
2. Run the tool to generate prompts for your weekly report
3. Use the generated prompt with your preferred LLM to create the actual report

## Output

The tool generates:
- A structured prompt file for LLM
- A template file for report formatting
- Historical tracking of previous reports
