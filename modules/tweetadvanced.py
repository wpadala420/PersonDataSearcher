import subprocess


with open('data.txt', 'w+') as file:
    subprocess.call(['python3', '../modules/tweets_analyzer/tweets_analyzer.py','-n','drdr_zz'], stdout=file)