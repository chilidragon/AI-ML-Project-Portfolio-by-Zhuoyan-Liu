'''
File contains code to address conditions:
- parse and write to RIS file
- sort records by 'publication_year' in RefMan (filter by date)
- sort records by 'type_of_reference' in RefMan (filter for journal entries and books)
- sort records by 'publisher' in RefMan (filter for approved or unknown publishers)
*Disclaimer: RefMan must be downloaded 
'''


import rispy
import os


journals = []
books = []
missing_date = []
unknown_type = []
pre_print = []


#approved_publishers = []
banned_publishers = ['Springer']


def parse_ris(filepath):
    '''
    Takes in absolute filepath of ris file with 1+ entires.
    Parses and returns ris file.
    '''
    with open(filepath, 'r', encoding="utf8") as bibliography_file:
        return rispy.load(bibliography_file)


def date_sort(parsed_ris):
    '''
    Takes in parsed ris file with 1+ entires.
    Returns list of entires with correct or empty publication year.
    '''
    correct_date = []
    for entry in parsed_ris:
        if 'publisher' not in entry.keys():
            missing_date.append(entry)
        elif entry['publication_year'] == '2022':
            correct_date.append(entry)
    return correct_date


def publishers_sort(parsed_ris):
    '''
    Takes in parsed ris file with 1+ entires.
    Returns list of entires publishers that are not known or not banned.
    *Manually filter for approved publishers.
    '''
    publisher_passes = []
    for entry in parsed_ris:
        if 'publisher' not in entry.keys() or entry['publisher'] not in banned_publishers:
            publisher_passes.append(entry)
    return publisher_passes


def journal_sort(parsed_ris):
    '''
    Takes in parsed ris file with 1+ entires.
    Returns list of entires that are journals.
    '''
    journals = []
    for entry in parsed_ris:
        if entry['type_of_reference'] == 'JOUR' or entry['type_of_reference'] == 'JFULL':
            journals.append(entry)
    return journals


def book_sort(parsed_ris):
    '''
    Takes in parsed ris file with 1+ entires.
    Returns list of entires that are books.
    '''
    books = []
    for entry in parsed_ris:
        if entry['type_of_reference'] == 'BOOK':
            books.append(entry)
    return books


def filter_pre_print(parsed_ris):
    '''
    Takes in parsed ris file with 1+ entires.
    Appends pre-print entries to global variable pre_print.
    '''
    for entry in parsed_ris:
        if 'number' in entry.keys() and entry['number'] == 'ahead-of-print':
            pre_print.append(entry)


def filter_types(filepath):
    '''
    Appends entries to global variable filtered_data
    after parsing ris file, organizing parsed ris file
    down to entires with the correct publication date and
    publishers that are unknown or not banned into journals
    or books along with entries with empty publication dates
    or are pre-print.
    '''
    parsed_ris = parse_ris(filepath)
    filter_pre_print(parsed_ris)
    date_filtered = date_sort(parsed_ris)
    publisher_filtered = publishers_sort(date_filtered)
    type_filtered = journal_sort(publisher_filtered) + book_sort(publisher_filtered)
    for entry in type_filtered:
        if entry not in pre_print:
            if entry['type_of_reference'] == 'JOUR' or entry['type_of_reference'] == 'JOUR':
                journals.append(entry)
            elif entry['type_of_reference'] == 'BOOK':
                books.append(entry)
            else:
                unknown_type.append(entry)


# we might be able to filter down by type_of_reference (includes whether the publication is an ebook vs. unpublished work
# as well as government document)
# we might be able to filter down by reviewed item, abstract
# after articles are sorted manually into technical and non-technical, we can filter down by page number
def main():
    # ris file with entry with correct publication year, not a journal
    # filter_data('/Users/wande/Downloads/ris_test2.ris')

    # ris file with no publication year, journal entry
    # filter_data('/Users/wande/Downloads/ris_test4.ris')

    # ris file with correct publication year, journal entry
    # filter_data('/Users/wande/Downloads/ris_test6.ris')

    # ris files downloaded after refmanDownloader is run
    for filename in os.listdir('/Users/wande/Downloads/Test'):
        filepath = '/Users/wande/Downloads/Test/' + filename
        filter_types(filepath)

    print(journals)
    print(books)
    print(missing_date)
    print(unknown_type)
    print(pre_print)

    with open('journals.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(journals, bibliography_file)
    with open('books.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(books, bibliography_file)
    with open('missing_date.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(missing_date, bibliography_file)
    with open('unknown_type.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(unknown_type, bibliography_file)
    with open('pre_print.ris', 'w', encoding="utf8") as bibliography_file:
        rispy.dump(pre_print, bibliography_file)


if __name__ == '__main__':
    main()