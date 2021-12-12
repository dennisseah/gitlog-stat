"""Generate statistics."""

from gitlog_stat.ingestor.ingestor import Ingestor
from gitlog_stat.ingestor.log_entry import LogEntry

from gitlog_stat.reports.standard import Standard
from gitlog_stat.reports.commit_by_day import CommitByDay
from gitlog_stat.reports.commit_by_time import CommitByTime
from gitlog_stat.reports.commit_by_week import CommitByWeek
from gitlog_stat.reports.commit_by_week_by_customer import CommitByWeekByCustomer


class Statistic:
    @staticmethod
    def build(project: str, files: list, print_rpt=True):
        result = Ingestor.ingest_from_file(files)
        df = LogEntry.to_dataframe(result)

        print()
        print(project)
        print()
        Standard().build(df, print_rpt=print_rpt)
        CommitByWeek().build(df, print_rpt=print_rpt)
        CommitByDay().build(df, print_rpt=print_rpt)
        CommitByTime().build(df, print_rpt=print_rpt)
        CommitByWeekByCustomer().build(df, print_rpt=print_rpt)

        return df
