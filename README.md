# surebets-finder

Try to find as much as possible sure bets on the bookmaker websites

## Setup

1. Install dependencies:

```bash
$ poetry install
```

2. Setup pre-commit hooks before committing:

```bash
$ poetry run pre-commit install
```

3. Export mongodb host name to env variable:

```bash
$ export MONGO_HOST=localhost
```

## Run

1. Run importer
```
$ poetry run python main.py
```

### Testing

1. Run mongodb:

```bash
$ docker-compose up
```

2. Run tests:

```bash
$ poetry run pytest
```
