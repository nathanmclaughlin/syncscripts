"""Script to export network account information in LDAP to a CSV file"""

import sys, csv, ldap, ldaphelper


def get_student_account_info(attributes):
    """Return a list of student account attributes."""
    pass

def output_to_csv(accountList):
    """Output list of accounts with attributes to CSV file"""
    pass

def main():
    """Main entry point for the script."""
    movies = get_top_grossing_movie_links(URL)
    with open('output.csv', 'w') as output:
        csvwriter = csv.writer(output)
        for title, url in movies:
            keywords = get_keywords_for_movie(
                'http://www.imdb.com{}keywords/'.format(url))
            csvwriter.writerow([title, keywords])


if __name__ == '__main__':
    sys.exit(main())
