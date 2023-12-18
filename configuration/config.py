from pydantic import BaseSettings
from datetime import datetime
import os


class StudentsSettings(BaseSettings):
    application: str = 'Students Management System'
    webmaster: str = 'sjctrags@napne.com'
    created = '2023-11-11'