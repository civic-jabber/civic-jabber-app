# Civic Jabber User App

Welcome to the Civic Jabber user app repo! This repository contains code for the user
facing tool, which allows users to discover the status of regulations and encourages
them to submit public comments.

## Installation

The easiest way to install the package is from the `Makefile`. You can use the following
command.

```
make pip-install
```

To run the UI local, you'll need to NPM install the dependencies for the user app, which
you can do with the following command. Do note, this assumes you have NPM already
install on your system.

```
make npm-install
```


### Adding Python dependencies

The package uses `pip-compile` to lock dependencies. If you need to add a new
dependency, simply update the appropriate `.in` file in the `requirements` folder and
then run `make pip-compile`.

## Running the UI localy

To run the UI locally, you can use the following command:

```
make run-ui-local
```

## Database

### Connections

The database connections utility manages connections to the database. To connect to a
specific database, set the following environmental variable:

```
CIVIC_JABBER_PG_HOST
CIVIC_JABBER_PG_PORT
CIVIC_JABBER_PG_DB
CIVIC_JABBER_PG_USER
```

If you do not set an environmental variable, it will assume a default value. You can
connect to the database with:

```python
from civic_jabber_ingest.utils.connection import connect

connection = connect()

```
