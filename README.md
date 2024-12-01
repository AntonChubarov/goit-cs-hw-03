# goit-cs-hw-03
## GOIT Computer Systems Homework 3

### Prerequisites
- Git
- Docker and Docker Compose
- Python 3
- Poetry


### Installation

Clone the repository:
```shell
git clone https://github.com/AntonChubarov/goit-cs-hw-03.git
```

Navigate to the project directory:
```shell
cd goit-cs-hw-03
```

Install the project dependencies using Poetry:
```shell
poetry install
```

### Usage

Build and start the Docker containers:
```shell
docker compose up -d --build
```

#### PostgreSQL

Create the database schema:
```shell
python3 ./postgres/setup_db.py
```

Populate the database with initial data:
```shell
python3 ./postgres/seed.py
```

Execute queries:
```shell
python3 ./postgres/queries.py
```

#### MongoDB

Run the MongoDB interaction script:
```shell
python3 ./mongo/main.py
```
