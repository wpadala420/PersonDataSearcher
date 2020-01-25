

def check_if_link_exist(links, link):
     for l in links:
        if l in link:
            return False
     return True