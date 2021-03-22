from permutations import email_permuter

def permutateEmail(name_and_surname, domain):
    split = name_and_surname.split(' ')
    return email_permuter.all_email_permuter(first_name=split[0], last_name=split[1], domain_name=domain)


print(permutateEmail('Wojciech Padala', 'gmail.com'))