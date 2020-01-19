'''
    # Extract all names from the textbook index text file \
    # given the file has clear line breaks (a line = an index)
    @Author: Luoying Chen
    @Email: lzc0050@auburn.edu
'''

'''
    # get the indexes whose first character is capitalized
    # delete the index signs such as '¥', 'o', and '•' and the space before the index
    # return the indexes whose first char is capitalized after its index signs are deleted
    #
    # Ex: "Acipenser, 360b " ---> "Acipenser, 360b "
    #     "¥ Bada, Jeffrey, 58 " ---> "Bada, Jeffrey, 58 "
    #     "in acoelomorphs, 185 " ---> None
    @param singleIndex - a string
    @return singleIndex - a capitalized string (index)
    @return cleanIndex - a string whose begining signs/spaces are removed and is cappitalized
'''
def cleanIndex(singleIndex):
    if the1stCharIsCap(singleIndex):
        return singleIndex
    
    spacePosi = singleIndex.find(' ')
    cleanIndex = singleIndex[(spacePosi + 1):]
    if (the1stCharIsCap(cleanIndex)):
        return cleanIndex
    
    return None


'''
    # determine if the first character of the string is uppercase
    @param clean - a string
    @return True if the string is capitalized
    @return False all else
'''
def the1stCharIsCap(clean):
    if (clean is not None) and (ord(clean[0]) >= 65) and (ord(clean[0]) <= 90):
        return True
    return False


'''
    # determine if the second character after the first comma is uppercase
    @param clean - a string
    @param commaPosi - an integer that is the index of the comma in the string
    @return True if the second character after the first comma is uppercase
    @return False all else
'''
def the2ndCharAfter1stCommaIsCap(clean, commaPosi):
    if (clean is not None) and the1stCharIsCap(clean[(commaPosi + 2):]):
        return True
    return False


'''
    # determine if the third character after the first comma is lowercase
    # Ex: Avery, Oswald, 315
    @param clean - a string
    @param commaPosi - an integer that is the index of the comma in the string
    @return True if the third character after the first comma is lowercase
    @return False all else
'''
def the3rdCharAfter1stCommaIsatoz(clean, commaPosi):
    if (clean is not None) and (ord(clean[commaPosi + 3]) >= 97) \
    and (ord(clean[commaPosi+3]) <= 122):
        return True
    return False


'''
    # determine if the third character after the first comma is a period
    # Ex: Carey, F. G., 354b
    @param clean - a string
    @param commaPosi - an integer that is the index of the comma in the string
    @return True if the third character after the first comma is a period
    @return False all else
'''
def the3rdCharAfter1stCommaIsPeroid(clean, commaPosi):
    if (clean is not None) and (clean[commaPosi + 3] == '.'):
        return True
    return False


'''
    # determine if the character before the first space is a comma
    # Ex: Avery, Oswald, 315 vs. Dead zone, Gulf of Mexico, 760f (remove the second case)
    @param clean - a string
    @return True if the character before the first space is a comma
    @return False all else
'''
def theCharBefore1stSpaceIsComma(clean):
    spacePosi = clean.find(' ')
    if (spacePosi != -1) and (clean[spacePosi - 1] == ','):
        return True
    return False

'''
    # determine whether a capitalized index is a name or not
    # Name Samples: Carey, F. G., 354b
    #               Avery, Oswald, 315
    #               Arnold, A. Elizabeth, 665f
    #               Darwin, Charles. See also Common descent theory; Darwinian evolutionary theory
    #
    # Not a Name: Dead zone, Gulf of Mexico, 760f
    #             Data, 17, 19f, 21Ð22, F-1ÐF-3
    #             Controlled experiments, 20Ð21, F-3
    #             Domains, taxonomy, E-1, 12f, 13, 458f, 552, 553f, 566, 567f, 584t.
    #             domain, E-1, 12f, 566, 567f, 584t, 585
    @param clean - a capitalized string (index)
    @return True if the index is a name
    @return Flase if the index is not a name
'''
def isName(clean):
    if (clean is not None):
        commaPosi = clean.find(',')
        if (commaPosi != -1):
            if the2ndCharAfter1stCommaIsCap(clean, commaPosi) and \
                theCharBefore1stSpaceIsComma(clean) and \
                (the3rdCharAfter1stCommaIsatoz(clean, commaPosi) or \
                 the3rdCharAfter1stCommaIsPeroid(clean, commaPosi)):
                return True
    return False


'''
    # get names from index
    @param indexList - the list of indices of the text file
    @return nameList - the list of the names of the text file
'''
def nameList(indexList):
    nameList = []
    for index in indexList:
        clean = cleanIndex(index)
        if (clean != None) and isName(clean):
            nameList.append(clean)
    return nameList;


'''
    # read index from a file and write names to another file
    @param fileReadAddr - the address of the index file in txt format
    @param nameWriteAddr - the address of the output file
'''
def getNames(fileReadAddr, nameWriteAddr):
    ENCODING = 'utf-8'
    txtFile = open(fileReadAddr, 'r', encoding = ENCODING)
    name = open(nameWriteAddr, 'w')
    nameList = nameList(txtFile)
    txtFile.close()
    name.write(x) for x in nameList
    name.close()
    print(True)


if __name__ == '__main__':
    # an example:
    fileReadAddr = '../textbooks/Biological Science_Index.txt'
    nameWriteAddr = '../NameLists_1/Name Freeman.txt'
    getNames(fileReadAddr, nameWriteAddr)

