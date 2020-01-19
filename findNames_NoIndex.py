'''
    # Extract all names from the textbook index text file \
    # given the file has clear line breaks (a line = an index)
    @Author: Luoying Chen
    @Email: lzc0050@auburn.edu
'''
import spacy
import string

'''
    # determine if the first character of the string is uppercase
    @param token - a word
    @return True if the string is capitalized
    @return False otherwise
'''
def the1stCharIsCap(token):
    if (ord(token[0]) >= 65) and (ord(token[0]) <= 90):
        return True
    return False


'''
    # determine if the second character is uppercase or is a period
    @param token - a word
    @return True if the second character is uppercase or is a period
    @return False otherwise
'''
def the2ndCharIsatozOrPeriod(token):
    if (len(token) > 1):
        if  ((ord(token[1]) >=97) and (ord(token[1]) <= 122)) or (token[1] == '.'):
            return True
    return False


'''
    # determine if a string is a name
    @param: a string that is regarded as a name by the NLP algorithm
    @return True if the string's format matches the format of a name
    @return False otherwise
'''
def isName(aString):
    
    # check if contains numbers
    for chara in aString:
        if (ord(chara) >= 48) and (ord(chara) <= 57): ## 0～9
            return False

    # check if there are 2 or 3 words (assume the first time each name appears,
    # it has first (middle) last name, and we only include its first appearance)
    x = aString.split();
    if (len(x) == 2) or (len(x) == 3):
        numTrue = 0
            # check if every token is capitalized and the second character is a period or a~z
            for chara in x:
                if the1stCharIsCap(chara) and the2ndCharIsatozOrPeriod(chara):
                    numTrue += 1
        if numTrue == len(x):
            return True

    return False


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')

    text = []
    # an example
    with open("../textbooks/Principles_of_Life.txt", "r", encoding = "utf-8") as Life:
        for page in Life:
            text.append(page)

    nameList = []
    namePage = []
    for pageNum in range(len(text):
        doc = nlp(text[pageNum])
        for entity in doc.ents:
            if (entity.label_ == "PERSON") and isName(entity.text) \
            and (entity.text not in nameList):
                nameList.append(entity.text)
                nameAndPage = entity.text + '' + str(pageNum + 1)
                    namePage.append(nameAndPage)

    # an example
    nameLife = open("NameLists/NoIndex Name Principle of Life.txt", "w")
    for i in range(0, len(namePage)):
        nameLife.write(namePage[i] + "\n")


