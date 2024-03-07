from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    db_user:str
    db_password:str 
    db_host:str 
    db_port:str 
    db_name:str 
    secret_key: str
    alg: str
    exp: int

    class Config:
        env_file= ".env"

settings =Settings()
