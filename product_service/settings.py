from dotenv import dotenv_values


config = dotenv_values(".env")

APP_PORT=int(config["APP_PORT"])

POSTGRES_USER=config["POSTGRES_USER"]
POSTGRES_PASSWORD=config["POSTGRES_PASSWORD"]
POSTGRES_HOST=config["POSTGRES_HOST"]
POSTGRES_PORT=int(config["POSTGRES_PORT"])
POSTGRES_DB=config["POSTGRES_DB"]