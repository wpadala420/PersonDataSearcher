import subprocess

def search_sherlock(nickname):
    results = []
    filename = '../tmp/sherlock/ ' + nickname + '.txt'
    with open(filename, 'w+') as file_write:
        subprocess.call(['python3', 'sherlock/sherlock.py', nickname, '--no-color'], stdout=file_write)

    with open(filename, 'r+') as file_read:
        for line in file_read:
            if line.find('[+]') != -1:
                elem = {}
                site_name = line.split(': ')[0].strip()
                site_url = line.split(': ')[1].strip()
                elem['site_name'] = site_name
                elem['site_url'] = site_url
                results.append(elem)

    return results

print(search_sherlock('drdr_zz'))
