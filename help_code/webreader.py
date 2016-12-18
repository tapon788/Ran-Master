import urllib2

url = 'https://www.python.org/'
username = 'tpaul'
password = 'Hosna2016'
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

page = urllib2.urlopen(url).read()