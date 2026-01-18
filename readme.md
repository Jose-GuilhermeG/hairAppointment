# hairAppointment
a simple api create to apply some topics about software architecture then i have been studied 
this system is used to managig hair cut appointments togheter get an appointement
the appointments are booked by date and hour and are genarete a limited number of them for day about the open hour and close hour of barbershop
the number of a appointment who can be booked for day is defined automatic with a simple calcule -> number_appointment = finish_at - started_at 
the duration of a appointment is defined automatic with a simple calcule -> appointment_duration = number_appointment / number_appointment
of course , both var is calculate as time

# How install:

## Requirements:
The system has some requirements to be install:
- git 
- python
- redis
- mysql or another database

those are the base system technologies and are need to it's works correctly

## Install:
1. clone repository:
```bash
    git clone https://github.com/Jose-GuilhermeG/hairAppointment ./<your_folder_name>
```

2. create env
```bash
    cd <your_folder_name>
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
```

3. install python requirements:
```bash
    pip install -r requirements/local.txt
```

4. create your .env file and set your enveriment vars
```bash
    cp ./.env-example ./.env
```

| Var | what it does|
| ----- | ----- |
| SECRET_KEY | used for the security system|
| DEBUG | define if the system is in debug mode | 
| DATABASE_USER |  your database username |
| DATABASE_PASSWORD | your database host password |
| DATABASE_HOST | your database host |
| DATABASE_NAME | your database name |
| DATABASE_PORT | your database port |
| DATABASE_ENGINE | the engine used to connect on database |
| REDIS_HOST | your redis host |
| REDIS_PASSWORD | your redis password|
| REDIS_PORT | your redis host port |

5. run it:
```bash
    uvicorn src.main:app --reload
```

