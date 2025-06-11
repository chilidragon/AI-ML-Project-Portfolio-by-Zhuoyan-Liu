'''
File contains code to address conditions:
- read pdf
- filter out publications with >4 pages
- filter out pre-print publications
- search for and filter by publication year in pdf
- write to RIS file with publications filtered by pdf
*Disclaimer: pdf must be downloaded
'''


import process_ris as pr
import PyPDF2 as pdf2
import rispy


pre_print_pdf = []
correct_date_pdf = []
correct_pages_pdf = []

pre_print_full = []


def read_page(filepath):
    '''
    Takes in absolute filepath of pdf file.
    Parses and returns text of first page in pdf as string.
    '''
    parsed_pdf = pdf2.PdfFileReader(filepath)
    first_page = parsed_pdf.pages[0]
    return " ".join(first_page.extractText().split())


def count_pages(filepath):
    '''
    Takes in absolute filepath of pdf file.
    Parses the pdf and returns the number of pages in the pdf.
    '''
    parsed_pdf = pdf2.PdfFileReader(filepath)
    return parsed_pdf.numPages


def filter_num_pages(filepath):
    '''
    Takes in absolute filepath of pdf file.
    Appends filepath to global variable correct_pages_pdf if it has
    greater than or equal to 4 pages.
    '''
    num_pages = count_pages(filepath)
    if num_pages >= 4:
        correct_pages_pdf.append(filepath)


def filter_pre_print(filepath):
    '''
    Takes in absolute filepath of pdf file.
    Searches for pre-print keywords on the first page of the parsed pdf file.
    Appends filepath to global variable pre_print_pdf if keyword is found.
    '''
    text = read_page(filepath)
    norm_text = text.lower()
    if 'pre-print' in norm_text or 'ahead-of-print' in norm_text or 'online only' in norm_text:
        pre_print_pdf.append(filepath)


def filter_date(filepath):
    '''
    Takes in absolute filepath of pdf file. If pdf has >= 4 pages and is not pre-print,
    searches for publication year on the first page of the parsed pdf file.
    Appends filepath to global variable correct_date_pdf if publication year is found.
    '''
    if filepath in correct_pages_pdf and filepath not in pre_print_pdf:
        if '2022' in read_page(filepath):
            correct_date_pdf.append(filepath)


def fill_missing_date(ris):
    '''
    Parses pdfs in the global variable correct_date_pdf.
    Parses ris file filtered and appends entry in file to global variable
    correct_date_full if primary_title in entry is found on the first page
    of each parsed pdf.
    '''
    parsed_ris = pr.parse_ris(ris)
    for entry in parsed_ris:
        title = entry['primary_title'].lower()
        #print(title)
        for pdf in correct_date_pdf:
            text = read_page(pdf).lower()
            if title in text:
                entry['publication_year'] == '2022'
    return parsed_ris


def write_pre_print_full(ris):
    '''
    Parses pdfs in the global variable correct_date_pdf.
    Parses ris file filtered and appends entry in file to global variable
    correct_date_full if primary_title in entry is found on the first page
    of each parsed pdf.
    '''
    parsed_ris = pr.parse_ris(ris)
    for entry in parsed_ris:
        title = entry['primary_title'].lower()
        #print(title)
        for pdf in pre_print_pdf:
            text = read_page(pdf).lower()
            if title in text:
                pre_print_full.append(entry)


def main():
    # check if pdf file has enough pages
    filter_num_pages('/Users/wande/Downloads/IEEE_TSC_Supporting_rapid_development_of_a_data_visualization_system_in_emergency_response.pdf')
    print(correct_pages_pdf)

    filter_pre_print('/Users/wande/Downloads/IEEE_TSC_Supporting_rapid_development_of_a_data_visualization_system_in_emergency_response.pdf')
    print(pre_print_pdf)
    write_pre_print_full('journals.ris')
    write_pre_print_full('books.ris')
    write_pre_print_full('unknown_type.ris')
    pre_print = pr.parse_ris('pre_print.ris')
    for entry in pre_print_full:
        pre_print.append(entry)
    print(pre_print)

    with open('pre_print.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(pre_print, bibliography_file)

    filter_date('/Users/wande/Downloads/IEEE_TSC_Supporting_rapid_development_of_a_data_visualization_system_in_emergency_response.pdf')
    print(correct_date_pdf)
    correct_date_filled = fill_missing_date('missing_date.ris')
    print(correct_date_filled)
    journals = pr.parse_ris('journals.ris')
    books = pr.parse_ris('books.ris')
    unknown_type = pr.parse_ris('unknown_type.ris')
    for entry in correct_date_filled:
        if entry['type_of_reference'] == 'JOUR' or entry['type_of_reference'] == 'JOUR':
            journals.append(entry)
        elif entry['type_of_reference'] == 'BOOK':
            books.append(entry)
        else:
            unknown_type.append(entry)
    print(journals)
    print(books)
    print(unknown_type)

    with open('journals.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(journals, bibliography_file)
    with open('books.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(books, bibliography_file)
    with open('unknown_type.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(unknown_type, bibliography_file)


if __name__ == '__main__':
    main()