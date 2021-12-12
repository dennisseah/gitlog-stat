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
        df_commit_by_time = (
            df[["author", "commit_time", "lines_total"]]
            .groupby(["author", "commit_time"])["lines_total"]
            .sum()
            .reset_index()
        )

        if print_rpt:
            self.print_report(df_commit_by_time)

        return df_commit_by_time

    def print_report(self, df_stat):
        """Print report.

        Args:
            df_stat (DataFrame): statistic dataframe.
        """
        unique_times = sorted(df_stat["commit_time"].unique().tolist())
        for author in df_stat["author"].unique().tolist():
            self._print_time_bar(author, unique_times, df_stat)
