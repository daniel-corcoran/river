from flask import Flask, render_template
from app import app, frontend
from testing import testing


if __name__ == "__main__":
    # Run all checks before starting the server.
    # It should throw an exception here if one of the unit tests fails.
    testing.run_all_prestartup_checks()
    app.run(port=8080, host='0.0.0.0')