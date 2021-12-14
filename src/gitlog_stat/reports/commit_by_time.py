"""Git Commit by Time Report Generator."""

from gitlog_stat.reports.report_base import ReportBase


class CommitByTime(ReportBase):
    """Git Commit by Time Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        return self._build_author_report(df, self._print_time_bar, "commit_time", print_rpt)
