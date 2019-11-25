import subprocess


with open('data.txt', 'w+') as file:
    subprocess.call(['python', './modules/tweets_analyzer/tweets_analyzer.py','-n','drdr_zz'], stdout=file)