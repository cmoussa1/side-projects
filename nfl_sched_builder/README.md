# NFL Schedule Builder

## Overview
The NFL Schedule Builder is a Python-based tool that generates a season
schedule for a specified NFL team. This program adheres to the official NFL
scheduling rules and ensures a balanced distribution of games, including
intra-division, intra-conference, and inter-conference matchups. Additionally,
the team is assigned a bye week between Weeks 5 and 14.

## Features
- Automatically generates a 17-game schedule for a specified NFL team.
- Ensures compliance with NFL scheduling rules:
  - Each team plays its divisional opponents twice (home and away).
  - Each team plays one division in their conference and one division in the other conference.
  - Includes 3 games against remaining available opponents.
  - Assigns a bye week between Week 5 and Week 14.
- Outputs the schedule in a clear and concise format.

## Prerequisites
- Python 3.8 or higher.

## Usage
Run the program from the command line with the team's name as an argument:

```bash
python nfl_schedule_builder.py "Team Name"
```
