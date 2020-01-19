'''
    # Convert a textbook file in .pdf format to .txt format
    @Author: Luoying Chen
    @Email: lzc0050@auburn.edu
'''

import PyPDF2
import string

'''
    # Convert a textbook file in .pdf format to .txt format
    @param pdfName - the address of the input pdf file
    @param textName - the address of the output txt file
    @param pageBegin - the beginning page
    @param pageEnd - the last page
'''
def pdfConvertTxt(pdfName, textName, pageBegin, pageEnd):
    
    pdfFileObj = open(pdfName, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    for page in range(pageBegin, pageEnd + 1):
        pageObj = pdfReader.getPage(page)
        text = pageObj.extractText() + '\n'
        
        textFile = open(textName, 'a')
        content = text.split()
        for word in content:
            textFile.write(" ")
            textFile.write(word)
            # 1 page = 1 line
            textFile.write("\n")
        textFile.close()
    
    pdfFileObj.close()


if __name__ == '__main__':
    # an exampple:
    pdfName = "../textbooks/Biological Science 5th Edition by Scott Freemanp.pdf";
    textName = "../textbooks/Biological Science 5th Edition by Scott Freemanp.txt";
    # convert from the first page of chapter 1 (p.42) to the last page of chapter 45 (p.976)
    pdfConvertTxt(pdfName, textName, 42, 976);
