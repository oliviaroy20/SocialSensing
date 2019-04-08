import csv
import os
import subprocess
import shutil

#with open("Senators.csv", "r") as f:
reader = ["BernieSanders", "SenatorStrange", "SenJohnMcCain", "SenFranken", "SenThadCochran"]
#reader = csv.reader(f, delimiter=";")
for i, row in enumerate(reader):
    #name = row[2].strip()
    name = row
    #if i < 79:
    #    continue
    subprocess.call(["python", "Exporter.py", "--querysearch", name, "--since" , "2017-07-01", "--until", "2017-07-25"])
    subprocess.call(["cp", "output_got.csv", "Senator_tweets/" + name + ".csv"])
