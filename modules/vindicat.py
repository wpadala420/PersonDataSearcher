import requests

def search_vindicat(name):
    results = []
    url = 'https://vcat.pl/gielda-dlugow/oferty/api/?draw=2&columns[0][data]=title&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=firm_name&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]={}&columns[1][search][regex]=false&columns[2][data]=city&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=claim_type&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=debts_sum&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=false&columns[4][search][value]=0%2C0&columns[4][search][regex]=false&columns[5][data]=for_sale&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=site_details&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&order[0][column]=0&order[0][dir]=desc&start=0&length=10000&search[value]=&search[regex]=false&_=1615275634918'.format(name.split(' ')[1])
    data_json = requests.get(url).json()
    for elem in data_json['packages']:
        name_part = name.split(' ')[0]
        surname_part = name.split(' ')[1]
        if elem['firm_name'].find(name_part) != -1 and elem['firm_name'].find(surname_part) != -1:
            results.append(elem)
    return results





