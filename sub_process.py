import subprocess
import time

while True:
    print("Running scripts...")

    # Run first.py
    subprocess.run(["python", "data_update.py"])

    subprocess.run(["python", "news.py"])


    # Run second.py
    subprocess.run(["python", "preprocess.py"])
    subprocess.run(["python", "Scoring and Ranking.py"])


    

    print("Waiting for 5 seconds...\n")
    time.sleep(5)  # Wait for 5 seconds before running again
