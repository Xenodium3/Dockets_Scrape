###########################
#   docketscrape.py
#   July 2019
#   Description: this demo code scrapes the information from the sample
#   PACER docket html file. It exports 14 variable to a csv file.
#   Author: Weixin Yang
###########################
from bs4 import BeautifulSoup
import csv
import requests

# open the source file located at the same directory as my python code
with open('sampledocket.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# We can also utilize request package to access to website
# source = request.get('http://somewebsite.com').text
# Do a for loop to read and append all the info to the csv file.

# prettify my soup
#print(soup.prettify())

# Open a csv file
csv_file = open('dockets_scrape.csv', 'w')

# Write the headers
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Court Name', 'Petition #', 'Date filed', 'Date terminated',
                     'Debtor dismissed', 'Joint debtor dismissed', 'Plan confirmed',
                     '341 meeting', 'Judge name', 'Type of bankruptcy',
                     'Voluntary or involuntary', 'Assert or not', 'Debtor Disposition',
                     'Joint debtor disposition'])

# Acquring the variables
# page title
pagetitle = soup.title.text

center = soup.find('center')
centerlist = center.b.font.get_text(strip=True, separator='\n').split('\n')

# Courtname is the second element in that list
courtname = centerlist[1]

# Petition Number is the third element in that list
petitionNum0 = centerlist[2]
petitionNum = petitionNum0.rsplit(" ", 1)[1]

# Content in the left table
tabletext = soup.find('table', cellspacing="1")
lefttablelist = tabletext.tbody.tr.td.font.get_text(strip=True, separator='\n').split('\n')
#print(lefttablelist)

# Judge Name
judgename = lefttablelist[1]

# Type of bankruptcy
typename0 = lefttablelist[2]
str = typename0.rsplit(" ", 1)[1]
typename = typename0.rsplit("      ", 1)[0]+str

# voluntary or involuntary
volornot = lefttablelist[3]

# asset or not
assertornot = lefttablelist[4]

# Debtor Disposition
debtor = lefttablelist[7]

#Joint debtor disposition
jointdebtor = lefttablelist[9]

# Content in the right table
righttable = soup.find('td', valign="top", align="right")
righttablelist = righttable.font.table.tbody.get_text(strip=True, separator='\n').split('\n')
#print(righttablelist)

# Date filed
date_filed = righttablelist[1]

# Date terminated
date_terminated = righttablelist[3]

# Debtor dismissed
date_debtor = righttablelist[5]

# Joint debtor dismissed
date_joint = righttablelist[7]

# Plan confirmed
date_plan = righttablelist[9]

# 341 meeting
date_341meeting = righttablelist[11]

print(tabletext.prettify())
print()
print("Title: ", pagetitle)
print("Court Name: ", courtname)
print("Petition #: ", petitionNum)
for i in range(0, len(righttablelist)-1, 2):
    print(righttablelist[i], ' ', righttablelist[i+1])
print("Judge's name: ", judgename)
print("Type of bankruptcy: ", typename)
print("Voluntary or involuntary: ", volornot)
print("Assert or not: ", assertornot)
print("Debtor Disposition: ", debtor)
print("Joint debtor disposition: ", jointdebtor)

# Try/Exception for catching errors
try:
    # otherwise pass
    pass
except Exception as e:
    raise e

print()

# Write them into the csv file we created
csv_writer.writerow([courtname, petitionNum, date_filed, date_terminated,
                     date_debtor, date_joint, date_plan, date_341meeting,
                     judgename, typename, volornot, assertornot, debtor,
                     jointdebtor])

csv_file.close()