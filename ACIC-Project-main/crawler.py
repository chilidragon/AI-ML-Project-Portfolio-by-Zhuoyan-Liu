from ast import keyword
from bs4 import BeautifulSoup
import requests, lxml, os, json
import csv
#import textract, re

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

keyword = input("Keyword: \n")
start_date = input("Starting Date(return if none): \n")
end_date = input("Ending Date(return if none): \n")
sort_by = input("Enter 0 for sorting by relevance, 1 for sorting for date: \n")

params = {
  "q": keyword,
  "hl": "en",
  "as_ylo": start_date,
  "as_yhi": end_date,
  "scisbd": sort_by
}

html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
soup = BeautifulSoup(html, 'lxml')

for pdf_link in soup.select('.gs_or_ggsm a'):
  pdf_file_link = pdf_link['href']
  print(pdf_file_link)
 # text = textract.process(pdf_file_link)
 # words = re.findall(r"[^\W_]+", text, re.MULTILINE)
 # print(len(words))

data = []

for result in soup.select('.gs_ri'):
  title = result.select_one('.gs_rt').text
  title_link = result.select_one('.gs_rt a')['href']
  publication_info = result.select_one('.gs_a').text
  snippet = result.select_one('.gs_rs').text
  cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
  related_articles = result.select_one('a:nth-child(4)')['href']
  try:
    all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
  except:
    all_article_versions = None

# fields = ['title', 'title link', 'publication info', 'snippet', 'cited_by', 'related_articles', 'all_article_versions'] 
# rows = [title, title_link, publication_info, snippet, f'https://scholar.google.com{cited_by}', f'https://scholar.google.com{related_articles}', f'https://scholar.google.com{all_article_versions}']
# filename = "result.csv"
# with open(filename, 'a', newline='') as csvfile: 
#     csvwriter = csv.writer(csvfile) 
#     csvwriter.writerow(fields)  
#     csvwriter.writerows(rows)

  data.append({
    'title': title,
    'title_link': title_link,
    'publication_info': publication_info,
    'snippet': snippet,
    'cited_by': f'https://scholar.google.com{cited_by}',
    'related_articles': f'https://scholar.google.com{related_articles}',
    'all_article_versions': f'https://scholar.google.com{all_article_versions}',
  })

print(json.dumps(data, indent = 2, ensure_ascii = False))