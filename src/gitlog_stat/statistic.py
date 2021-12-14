"""Generate statistics."""

import json
import sys

from gitlog_stat.config import Config

from gitlog_stat.ingestor.ingestor import Ingestor
from gitlog_stat.ingestor.log_entry import LogEntry

from gitlog_stat.reports.standard import Standard
from gitlog_stat.reports.commit_by_day import CommitByDay
from gitlog_stat.reports.all_commit_by_day import AllCommitByDay
from gitlog_stat.reports.commit_by_time import CommitByTime
from gitlog_stat.reports.commit_by_week import CommitByWeek
from gitlog_stat.reports.commit_by_week_by_customer import CommitByWeekByCustomer


class Statistic:
    """This class is responsible for generating all the available statistics."""

    @staticmethod
    def build(project: str, files: list):
        """Build statistics.

        Args:
            project (str): Title of project.
            files (list): List of file paths that contains 'git log --stat' data.

        Returns:
            DataFrame: data frame for raw data.
        """
        print_rpt = True
        result = Ingestor.ingest_from_file(files)
        df = LogEntry.to_dataframe(result)

        print()
        print(project)
        print()
        Standard().build(df, print_rpt=print_rpt)
        CommitByWeek().build(df, print_rpt=print_rpt)
        CommitByDay().build(df, print_rpt=print_rpt)
        AllCommitByDay().build(df, print_rpt=print_rpt)
        CommitByTime().build(df, print_rpt=print_rpt)
        CommitByWeekByCustomer().build(df, print_rpt=print_rpt)

        return df

    @staticmethod
    def build_from_json(json_path: str):
        """Build statistics from json input.

        Args:
            json_path (str): path to JSON file
        """
        with open(json_path) as f:
            props = json.loads(f.read())
            Statistic.build(props["project"], props["files"])


if __name__ == "__main__":
    Config.parse()
    if len(sys.argv) != 2:
        print("Usage: python gitlog_stat/statistic.py <JSON file path>")
    else:
        Statistic.build_from_json(sys.argv[1])
