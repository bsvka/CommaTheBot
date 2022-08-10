from olclient.bots import AbstractBotJob as ol_helper
from olclient.openlibrary import OpenLibrary
from collections import namedtuple

import copy
import gzip
import re
import argparse
import sys


def save(save_fn) -> None: # olclient/bots.py
    global changed
    """
    Modify behavior of OpenLibrary Client based on 'limit' and 'dry_run' parameters
    :param save_fn: Save function of an OpenLibrary Client record (Work, Edition, Author)
    """
    if not dry_run:
        logger.info(save_fn())
    else:
        logger.info('Modification not made because dry_run is True.')
    changed += 1
    if limit and changed >= limit:
        logger.info('Modification limit reached. Exiting script.')
        sys.exit()

def needs_fixing(edition_title: str) -> bool:
    if edition_title is None: return False # no title given

    return True if(pattern.search(edition_title)) else False

def fix_title(edition_title: str) -> str:
    match = pattern.search(edition_title)

    return f"{match.group(2)} {match.group(1)}"

def run(filtered_file: str):
    with gzip.open(filtered_file, 'rb') as file:
        for row in file:
            row, json_data = ol_helper.process_row(row)
            if not needs_fixing(json_data.get('title')): # .get() to avoid KeyError
                continue

            # the database may have changed since the dump was created, so call the OpenLibrary API and check again
            olid = json_data['key'].split('/')[-1]
            isEdition = json_data['type']['key'] == '/type/edition'
            book = ol.Edition.get(olid) if isEdition else ol.Work.get(olid)

            if not ( book.type['key'] == '/type/edition' or book.type['key'] == '/type/work' ):
                continue # skip deleted books
            if not needs_fixing(book.title):
                continue

            # this book needs fixing
            old_title = copy.deepcopy(book.title)
            book.title = fix_title(book.title)

            logger.info(f'{olid}: "{old_title}" -> "{book.title}"')
            save(lambda: book.save(comment=comment))


comment = 'foo, the -> the foo'
articles = [
    '[Tt]he',
    '[Dd]er', '[Dd]ie', '[Dd]as',
    '[Ll]e', '[Ll]a', '[Ee]l',
    '[Ll]os', '[Ll]as', '[Ll]es',
]
pattern = re.compile(rf"^([\w ,]+), ?({'|'.join(articles)})$")
logger, console_handler = ol_helper.setup_logger("CommaTheBot")

Credentials = namedtuple('Credentials', ['username', 'password'])
ol = OpenLibrary()
#ol = OpenLibrary(credentials=Credentials("""""", """"""))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CommaTheBot')
    parser.add_argument('-f', '--file', help='Filtered OL dump to search in')
    parser.add_argument('-l', '--limit', type=int, default=1,
                                help='Limit number of edits performed on external data.'
                                    'Set to zero to allow unlimited edits.')
    parser.add_argument('-d', '--dry-run', type=ol_helper._str2bool, default=True,
                                help='Execute the script without performing edits on external data.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    dry_run = getattr(args, 'dry_run', None)
    limit = getattr(args, 'limit', None)
    changed = 0

    run(args.file)