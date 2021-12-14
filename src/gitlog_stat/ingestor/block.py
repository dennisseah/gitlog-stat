"""Single block of log entry."""

import datetime
import re

from gitlog_stat.config import Config
from gitlog_stat.ingestor.employee import Employee
from gitlog_stat.ingestor.log_entry import LogEntry


class Block:
    """Single block of log entry."""

    def __init__(self, s: str):
        """Instantiate an instance of this class.

        Args:
            s (str): initial string
        """
        self.data = []
        self.data.append(s)
        self.merged = False

    def author(self):
        """Return author.

        Returns:
            [str]: Author
        """
        mappings = Config.name_mappings

        for line in self.data:
            m = re.search(r"^Author:\s(.+?)\s<", line)
            if m:
                lc_name = m.group(1).lower()
                name = " ".join(map(lambda x: x.capitalize(), lc_name.split(" ")))
                return mappings[name] if name in mappings else name
                return name
        return None

    def title(self):
        """Return title of the person.

        Returns:
            [str]: Title
        """
        titles = Config.employee_titles
        name = self.author()
        return titles[name] if name is not None and name in titles else None

    def email(self):
        """Return email address.

        Returns:
            [str]: email address
        """
        for line in self.data:
            m = re.search(r"^Author:\s.+?\s<(.+?)>", line)
            if m:
                return m.group(1).lower()
        return None

    def is_customer(self):
        """Return True if the author is customer.

        Returns:
            [bool]: True if the author is customer.
        """
        email = self.email()
        if not email:
            return False

        return not any(
            [x in email for x in Config.company_email_domains]
        ) and not Employee.is_employee(email)

    def commit_time(self):
        """Return commit time.

        Returns:
            [datetime]: Commit time
        """
        for line in self.data:
            m = re.search(r"^Date:\s+(.+)", line)
            if m:
                return datetime.datetime.fromtimestamp(int(m.group(1)))

        return None

    def commit_stat(self):
        """Get commit statistics.

        Returns:
            dict: map of statistic to value.
        """
        result = {
            "files_changed": 0,
            "lines_added": 0,
            "lines_deleted": 0,
        }
        for token in self.data[-1].split(","):
            t = token.strip()

            m = re.search(r"(\d+)\sfile(s?) changed", t)
            if m:
                result["files_changed"] = int(m.group(1))
            else:
                m = re.search(r"(\d+)\sinsertion(s?)\(\+\)", t)
                if m:
                    result["lines_added"] = int(m.group(1))
                else:
                    m = re.search(r"(\d+)\sdeletion(s?)\(\-\)", t)
                    if m:
                        result["lines_deleted"] = int(m.group(1))

        return result

    def files_touched(self):
        """Get a list of modified (added, deleted, and modified) files.

        Returns:
            list: a list of modified files.
        """
        files = list(
            filter(lambda x: re.match(r"^\s[^\s]", x) and not re.match(r"^\s\s\s\s", x), self.data)
        )[:-1]

        return list(map(lambda x: x.split("|")[0].strip(), files))

    @staticmethod
    def parse(s: str):
        """Parse a stream of git log into log entries.

        Args:
            s (str): log stream.
        """
        results = []
        cur_block = None

        for line in s.splitlines():
            if re.match(r"^commit [a-f\d]+$", line):
                cur_block = Block(line)
                results.append(cur_block)
            elif re.match(r"^Merge: [a-f\d]", line):
                cur_block.merged = True
            elif len(line) > 0:
                cur_block.data.append(line)

        return list(map(lambda x: LogEntry(x), filter(lambda x: not x.merged, results)))
