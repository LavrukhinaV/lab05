import typer

def main(
    name: str = typer.Argument("Viktoriia", help="Имя пользователя."),
    lastname: str = typer.Option("", "--lastname", help="Фамилия пользователя."),
    formal: bool = typer.Option(False, "--formal", "-f", help="Использовать формальное приветствие."),
) -> None:
    if formal:
        typer.echo(f"Добрый день, {name} {lastname}!")
        return
    typer.echo(f"Привет, {name}!")

if __name__ == "__main__":
    typer.run(main)
