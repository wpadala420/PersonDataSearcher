import subprocess


def get_report(nickname):
    filename = nickname + '.txt'
    with open(filename, 'w+') as file:
        subprocess.call(['python3', 'modules/tweets_analyzer/tweets_analyzer.py', '-n', nickname, '--friends'],
                        stdout=file)

