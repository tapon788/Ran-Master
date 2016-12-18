import requests

proxies = {
  'http': 'http://tpaul:Hosna2016@172.16.1.246:8080',
  'https': 'https://tpaul:Hosna2016@172.16.1.246:8080',
}

r = requests.get('http://tigerslounge/Main/Home.aspx', auth=('tpaul', 'Hosna2016'))

#r = requests.get('http://tigerslounge/Main/Home.aspx', proxies=proxies)
if r.status_code == requests.codes.ok:
    print(r.headers['content-type'])

print r.text