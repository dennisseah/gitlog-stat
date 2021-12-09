"""Git Commit by Week Report Generator."""

from gitlog_stat.reports.report_base import ReportBase


class CommitByWeek(ReportBase):
    """Git Commit by Week Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        df_commit_per_week = (
            df[["author", "week_of_year", "lines_total"]]
            .groupby(["author", "week_of_year"])["lines_total"]
            .sum()
            .reset_index()
        )

        if print_rpt:
            self.print_report(df_commit_per_week)

        return df_commit_per_week

    def print_report(self, df_stat):
        """Print report.

        Args:
            df_stat (DataFrame): statistic dataframe.
        """
        unique_weeks = df_stat["week_of_year"].unique().tolist()
        for author in df_stat["author"].unique().tolist():
            self._print_week_bar(author, unique_weeks, df_stat)
