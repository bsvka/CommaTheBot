# example invocation
# python article_finder.py --file ol_dump_2022-06-06.txt.gz

from olclient.bots import AbstractBotJob
import gzip
import re

class Job_The(AbstractBotJob):
    pattern = re.compile(r"^([\w ,]*), ?([a-zA-Z]{1,4})$")

    def needs_fixing(self, edition_title: str) -> bool:
        return True if(self.pattern.search(edition_title)) else False

    def find_article(self, edition_title: str) -> str:
        match = self.pattern.search(edition_title)

        return match.group(2)

    def run(self) -> None:
        self.dry_run_declaration()

        with gzip.open(self.args.file, 'rb') as file:
            for row in file:
                row, json_data = self.process_row(row)
                if not ( json_data['type']['key'] == '/type/edition' or json_data['type']['key'] == '/type/work' ):
                    continue
                title = json_data.get('title') if json_data.get('title') else '' # title or ''
                if not self.needs_fixing(title):
                    continue

                self.logger.info(self.find_article(title))


if __name__ == "__main__":
    job = Job_The()

    try:
        job.run()
    except Exception as e:
        job.logger.exception("")
        raise e
