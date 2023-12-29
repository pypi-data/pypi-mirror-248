import typer

app = typer.Typer(help="Yi Jing Cli Tool", no_args_is_help=True)


@app.command(no_args_is_help=True)
def main():
    """
    Yi Jing Cli Tool
    """
    print(f"Yi Jing Cli Tool")


if __name__ == "__main__":
    app()
