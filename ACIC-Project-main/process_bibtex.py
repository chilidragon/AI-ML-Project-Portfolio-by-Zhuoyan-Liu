'''
Created: 11/07/2022
File contains code to address conditions:
- read bibtexs for each search result from URL
- write bibtexs for all search results into one .bib file
- write .bib file to .csv file
*Disclaimer: url list should be generated by another script
'''

import requests
import bibtexparser as btp
import pandas as pd

urls = ["https://scholar.googleusercontent.com/scholar.bib?q=info:y_pE6M2iY6YJ:scholar.google.com/&output=citation&scisdr=CgXGu4SxEKiQ8pTGRXo:AAGBfm0AAAAAY2vDXXpUn-8jmNLx4PMNI6QirhHOYyC4&scisig=AAGBfm0AAAAAY2vDXeqSZ4mKcNO2NeVcUC5vvpgnbtOr&scisf=4&ct=citation&cd=-1&hl=en"]

def compile_bibtexs(urls):
  '''
  Reads bibtexes from each URL in url list and
  writes all bibtexes into a single .bib file
  '''
  with open('bibtexs.bib', 'w') as bibtex_file:
    for bibtex in urls:
      bibtex_file.write(requests.get(bibtex).text)

def bibtex_to_csv():
  '''
  Loads bibtexes and writes bibtexes into a .csv file
  '''
  with open('bibtexs.bib') as bibtex_file:
    database = btp.load(bibtex_file)
  
  df = pd.DataFrame(database.entries)
  df.to_csv('bibtexs.csv', index=False)

def main():
  compile_bibtexs(urls)
  bibtex_to_csv()

if __name__ == '__main__':
    main()

# columns=['type', 'title', 'year', 'journal', 'publisher', 'pages']
# df = pd.DataFrame()

# for i in df.columns:
#   df[i] = 

# for row in database.entries:
#   print(row['ENTRYTYPE'])
#   df['type'] = row['ENTRYTYPE']
#   df['title'] = row['title']
#   df['year'] = row['year']
#   df['journal'] = row['journal']
#   df['publisher'] = row['publisher']
#   df['pages'] = row['pages']
  