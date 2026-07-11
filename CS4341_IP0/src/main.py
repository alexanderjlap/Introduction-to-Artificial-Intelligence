import click

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", help="Name of the greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    hello()