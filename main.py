import asyncio
import typer
from fastapi import FastAPI

from database import init_models
from views import router

app = FastAPI()
app.include_router(router, prefix="/vk")

cli = typer.Typer()

@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")

if __name__ == "__main__":
    cli()