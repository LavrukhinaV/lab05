import typer
import requests
from flask import Flask

app = Flask(__name__)
cli = typer.Typer()

@app.route("/")
def index():
    return "Hello AppSec World from Flask!"

@cli.command()
def greet(
    name: str = typer.Argument("Viktoriia", help="Имя пользователя"),
    lastname: str = typer.Option("", "--lastname", help="Фамилия пользователя"),
    formal: bool = typer.Option(False, "--formal", "-f", help="Формальное приветствие"),
):
    if formal:
        typer.echo(f"Добрый день, {name} {lastname}!")
    else:
        typer.echo(f"Привет, {name}!")

@cli.command()
def fetch(url: str = "https://example.com"):
    """HTTP-запрос к внешнему ресурсу"""
    response = requests.get(url, timeout=5)
    typer.echo(f"GET {url} -> {response.status_code}")

@cli.command()
def serve():
    """Запуск Flask-сервиса"""
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    cli()
