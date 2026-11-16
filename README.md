# Robo Swarm project

A Django project with 7 models and a REST API (Django REST Framework).

## Tech stack

- Python 3
- Django
- Django REST Framework
- psycopg2 (PostgreSQL)
- Pillow
- Database: PostgreSQL

## Project structure

- `roboSwarm_project/roboSwarm_project/`: project settings and root URLs
- `roboSwarm_project/drone_app/`: Django app
- `roboSwarm_project/mission_app/`: Django app
- `roboSwarm_project/robot_app/`: Django app
- Tests: `roboSwarm_project/drone_app/tests.py`, `roboSwarm_project/mission_app/tests.py`, `roboSwarm_project/robot_app/tests.py`

## Data model

| Model | App | Fields |
|---|---|---|
| `Drone` | `roboSwarm_project/drone_app` | id, name, serial_number, battery_level, max_speed, max_altitude, is_autonomous, payload_capacity |
| `TechnicalSpecification` | `roboSwarm_project/mission_app` | id, robot, drone, cpu, memory_gb, firmware_version |
| `Mission` | `roboSwarm_project/mission_app` | id, name, description, start_time, end_time, status |
| `Task` | `roboSwarm_project/mission_app` | id, mission, title, priority, is_completed |
| `MissionParticipation` | `roboSwarm_project/mission_app` | mission, agent_id, role, assigned_at |
| `TelemetryRecord` | `roboSwarm_project/mission_app` | agent_id, timestamp, data |
| `Robot` | `roboSwarm_project/robot_app` | id, name, serial_number, battery_level, max_speed, is_active, created_at |

## URL routes

Declared in `urls.py`:

- `/blog/`
- `/api/`
- `/robots/ (router)`
- `/drones/ (router)`
- `/technical-specifications/ (router)`
- `/missions/ (router)`
- `/tasks/ (router)`
- `/mission-participations/ (router)`
- `/telemetry-records/ (router)`

## How to run

```bash
cd roboSwarm_project
pip install pipenv
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

`settings.py` is configured for PostgreSQL: create the database and use your own credentials before running `migrate`.

Then open `http://127.0.0.1:8000/`.

---

Author: [Chaouki Bayoudhi](https://github.com/ChaoukiBayoudhi)
