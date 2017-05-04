from bs4 import BeautifulSoup
import requests
import time
import difflib
from difflib import *
from slacker import Slacker

slackapikey = 'xoxb-168765462614-AF2fvGqqzsTorz0BTvzXaEYu'

headerz = {
    'Connection': 'keep-alive',
    'Host': 'www.adidas.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
                }

slack = Slacker(slackapikey)
print "Monitor Started..."
while True:

    req = requests.Session()



    url = 'http://www.adidas.com/on/demandware.static/-/Sites-CustomerFileStore/default/adidas-US/en_US/sitemaps/product/adidas-US-en-us-product.xml'


    response = req.get(url, headers=headerz)
    ya = response.text
    
    token = BeautifulSoup(response.text, "lxml")

    
    with open('xmlparsing2.txt', 'w') as f:
        for option in token.find_all('loc'):
            f.write(option.text + "\n")
        f.close()


    yah = open('xmlparsing2.txt', 'r') 
    bruh = yah.read()
        
    answ = open('xmlparsing.txt', 'r')
    answr = answ.read()
    
    if answr == bruh:
        print '--No New Changes--'



    elif answr != bruh: 
        lines1 = answr.strip().splitlines()
        lines2 = bruh.strip().splitlines()
        
        diff = difflib.unified_diff(lines1, lines2, fromfile='xmlparsing2.txt', tofile='xmlparsing.txt', lineterm='', n=0)
        lines = list(diff)[2:]
        added = [line[1:] for line in lines if line[0] == '+']
        removed = [line[1:] for line in lines if line[0] == '-']

        print '--------------------------------'
        print 'Additions:'
        print '--------------------------------'
        for line in added:
            if line not in removed:
                
                headers = {
                    'Connection': 'keep-alive',
                    'Host': 'www.adidas.com',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
                }
                

                aco = req.get(line, headers=headers)
                soup = BeautifulSoup(aco.text, 'lxml')
                pidstep1 = line.split('/')
                pidstep2 = pidstep1[5]
                pidstep3 = pidstep2.split('.')
                pid = pidstep3[0]
                titleofproduct = soup.title.string
                print "ADDED:"
                print line    
                slack.chat.post_message('#adimon', "ADDED:\n" + titleofproduct + "  -  " + pid + "\nLink: \n" + line + "\n -------------------------------------------") 
                    
                
                






        
        ans = open('xmlparsing.txt', 'w')
        for option in token.find_all('loc'):
            ans.write(option.text + "\n")
        ans.close()
    
    yah.close()
    answ.close()
    time.sleep(1)