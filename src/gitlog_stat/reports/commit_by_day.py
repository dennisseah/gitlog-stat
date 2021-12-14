"""Git Commit by Day Report Generator."""

from gitlog_stat.reports.report_base import ReportBase


class CommitByDay(ReportBase):
    """Git Commit by Day Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        return self._build_author_report(
            df, self._print_day_bar, "commit_day", print_rpt, days=True
        )
