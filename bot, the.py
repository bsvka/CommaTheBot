# example invocation
# python bot, the.py --file ol_dump_2022-06-06.txt.gz --limit 1

from olclient.bots import AbstractBotJob
import copy
import gzip
import re

class Job_The(AbstractBotJob):
    @staticmethod
    def needs_fixing( edition_title: str ) -> bool:
        if edition_title == None: return False

        match = re.search("^[\w ,]*, ?[Tt]he$", edition_title)

        return False if(match == None) else True

    @staticmethod
    def fix_title( edition_title: str ) -> str:
        match = re.search("^([\w ,]*), ?([Tt]he)$", edition_title)

        return " ".join([match.group(2), match.group(1)])

    def run(self) -> None:
        self.dry_run_declaration()

        comment = 'foo, the -> the foo'
        with gzip.open(self.args.file, 'rb') as file:
            for row in file:
                row, json_data = self.process_row(row)
                if not ( json_data['type']['key'] == '/type/edition' or json_data['type']['key'] == '/type/work' ):
                    continue
                if not self.needs_fixing(json_data.get('title')): # .get() to avoid KeyError
                    continue

                # the database may have changed since the dump was created, so call the OpenLibrary API and check again
                olid = json_data['key'].split('/')[-1]
                book = self.ol.Edition.get(olid) if json_data['type']['key'] == '/type/edition' else self.ol.Work.get(olid)

                if not ( book.type['key'] == '/type/edition' or book.type['key'] == '/type/work' ):
                    continue # skip deleted books
                if not self.needs_fixing(book.title):
                    continue

                # this book needs editing, so fix it
                old_title = copy.deepcopy(book.title)
                book.title = self.fix_title(book.title)

                self.logger.info(f'{olid}: "{old_title}" -> "{book.title}"')
                self.save(lambda: book.save(comment=comment))


if __name__ == "__main__":
    job = Job_The()

    try:
        job.run()
    except Exception as e:
        job.logger.exception("")
        raise e
