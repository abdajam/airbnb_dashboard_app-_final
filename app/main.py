from controller import AppController
import sys
import os
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = AppController()
    app.run()
