from rich.console import Console

console = Console(soft_wrap=False, width=200)

def log(*args, **kwargs):
    console.print(*args, **kwargs)