import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

dirs = [os.path.join(BASE_DIR, nome) for nome in os.listdir(BASE_DIR)]
print(dirs)