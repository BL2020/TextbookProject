import re
import csv
from tqdm import tqdm
import lxml.etree
import urllib.parse, urllib.request

with open('../Role Models in Biology Textbooks - Data Set With Duplicates.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    names = []
    for row in readCSV:
        names.append(row[2])
csvfile.close()

del names[0]
del names[-1]

birth_date = []
birth_year = []

## test cases
names_no = ['Arkhat Abzhanov', 'Yu Chen']
names_redirect = ['Jun Li', 'Hilda Mangold', 'Linda Buck', 'Rosemary Grant', 'Matt Wilson']
names_multi = ['Stanley Cohen', 'Jun Li', 'William Hamilton']
names_table = ['Osamu Shimomura', 'Motoo Kimura', 'Elaine Ostrander']
names_text = ['Reiji Okazaki', 'Sarah Tishkoff', 'Elba Serrano','Reiji Okazaki', 'Charles Sibley']
names_others = ['Isaac Newton', 'James Hutton', 'Hilde Mangold']

def getText(name):

    params = { "format":"xml", "action":"query", "prop":"revisions", \
               "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.parse.quote(name.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.request.urlopen(url))
    revs = tree.xpath('//rev')
    text = revs[-1].text

    return text


def findBirthInMainText(text):
   
    birth_date0 = 'Birth Not Found in Wiki Page\n'
    birth_year0 = 'Birth Not Found in Wiki Page\n'


    date_index = text[:400].find('born')
    if date_index != -1:
        text = text[date_index + 5 : date_index + 30].replace(')',' ').replace('<',' ')
        numbers = [int(s) for s in text.replace(',',' ').split() if s.isdigit()]
        birth_date0 = text[: date_index + 20] + '\n'
        for number in numbers:
            if number > 1000:
                birth_year0 = str(number) + '\n'
                break
    else:
        date_index_start = text[:400].find('(')

        if date_index_start != -1:
            text = text[date_index_start + 1 : date_index_start + 35]
            date_index_end = min([text.find(')'), text.find('<'), text.find('–'), len(text)])
            text = text[:date_index_end]
            birth_date0 = text
            numbers = [int(s) for s in text.replace(',',' ').split() if s.isdigit()]
            for number in numbers:
                if number > 1000:
                    birth_year0 = str(number) + '\n'
                    break

    return birth_date0, birth_year0



for name in tqdm(names):

    text = getText(name)
    #print(name)
    #print(text[:300])   
    
    if text[:9].upper() == "#REDIRECT":
        begin = 12
        end = text.index("]]")
        redirect = text[begin : end]
        #print(redirect)
        if redirect.upper() == "APPLICATION PROGRAMMING INTERFACE":
            birth_date.append("Page Not Found\n")
            birth_year.append("Page Not Found\n")
            continue
        elif "(DISAMBIGUATION)" in redirect.upper():
            birth_date.append("Name Not Clear\n")
            birth_year.append("Name Not Clear\n")
            continue
        else:
            text = getText(redirect)
            #print(redirect)
            #print(text[:300])

            if text[:9].upper() == "#REDIRECT":
                begin = 12
                end = text.index("]]")
                redirect = text[begin : end]
                if redirect.upper() == "APPLICATION PROGRAMMING INTERFACE":
                    birth_date.append("Page Not Found\n")
                    birth_year.append("Page Not Found\n")
                    continue



    if ('may refer to:' in text[:200]) or ('is the name of:' in text[:200]):
        birth_date.append("Found Multiple People\n")
        birth_year.append("Found Multiple People\n")
        continue

    table_index = text.find("Infobox")
    
    if table_index != -1:
        sci_index = text.find("Infobox scientist")
        if sci_index != -1:
            
            birth_index = text.find("birth_date")
        
            if birth_index != -1:
                info = text[birth_index : birth_index + 60]
                j = info.find("|")
                jj = info.find("}")
            
                if j == -1 or jj == -1:
                    #print(info)
                    birth_date.append("Check\n")
                    birth_year.append("Check\n")
                    continue
                else:
                    date = info[j+1 : jj]
                    birth_date.append(date + '\n')
                    year_index = date.find("1")
                
                    if year_index == -1:
                        birth_year.append("YYYY\n")
                        continue
                    else:
                    
                        if ord(date[year_index + 2]) >= 48 and ord(date[year_index + 2]) <= 57:
                            birth_year.append(date[year_index : year_index + 4] + '\n')
                            continue
                        else:
                            birth_year.append(date[-4:] + '\n')
                            continue
            else:
                text_index = text[sci_index:].find('}}')
                text = text[text_index + 2 : ]
                birth_date0, birth_year0 = findBirthInMainText(text)
                birth_year.append(birth_year0)
                birth_date.append(birth_date0)
                
                if birth_date0 == 'Birth Not Found in Wiki Page\n' or \
                   birth_year0 == 'Birth Not Found in Wiki Page\n':
                    #print(name)
                    #print(text[:400])
                continue
        else:
            text = text[table_index:]
            occu_index = text.find('|')
            occu = text[8 : occu_index - 1]
            birth_year.append("May Not Be Scientist. " + occu + '\n' )
            birth_date.append("May Not Be Scientist. " + occu + '\n')
            continue
    birth_date0, birth_year0 = findBirthInMainText(text)
    birth_year.append(birth_year0)
    birth_date.append(birth_date0)
    
    if birth_date0 == 'Birth Not Found in Wiki Page\n' or \
       birth_year0 == 'Birth Not Found in Wiki Page\n':
        #print(name)
        #print(text[:400])


file1 = open('birth_date.txt', 'w')
file1.writelines(birth_date)
file1.close()

file2 = open('birth_year.txt', 'w')
file2.writelines(birth_year)
file2.close()

#print(len(birth_date))

