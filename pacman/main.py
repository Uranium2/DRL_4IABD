from app_class import *
from settings import *
import os.path
from os import path

if __name__ == "__main__":
    if not path.exists(FOLDER_PATH + "/high_score.txt"):
        with open(FOLDER_PATH + "/high_score.txt", "w") as f:
                f.write("0")
    app = App()
    app.run()
