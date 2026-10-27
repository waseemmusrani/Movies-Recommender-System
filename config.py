"""Configuration: the TMDB API key is read from an environment variable.

Never hard-code secrets in source files. Put the key in a local `.env`
file (ignored by Git), see `.env.example`.
"""
import os

from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into the environment

API_KEY = os.getenv("TMDB_API_KEY", "")
