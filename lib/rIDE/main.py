from flask import Flask, render_template
from app import app, frontend


if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0')