"""Git Commit by Day Report Generator."""

from gitlog_stat.reports.report_base import ReportBase

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


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
        df_commit_by_day = (
            df[["author", "commit_day", "lines_total"]]
            .groupby(["author", "commit_day"])["lines_total"]
            .sum()
            .reset_index()
        )

        if print_rpt:
            self.print_report(df_commit_by_day)

        return df_commit_by_day

    def print_report(self, df_stat):
        """Print report.

        Args:
            df_stat (DataFrame): statistic dataframe.
        """
        unique_days = sorted(df_stat["commit_day"].unique().tolist(), key=DAYS.index)
        for author in df_stat["author"].unique().tolist():
            self._print_day_bar(author, unique_days, df_stat)
