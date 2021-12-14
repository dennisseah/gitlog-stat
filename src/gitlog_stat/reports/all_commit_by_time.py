"""All Git Commit by Time Report Generator."""

from gitlog_stat.reports.report_base import ReportBase


class AllCommitByTime(ReportBase):
    """All Git Commit by Time Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        df_stat = (
            df[["commit_time", "lines_total"]]
            .groupby(["commit_time"])["lines_total"]
            .sum()
            .reset_index()
        )

        if print_rpt:
            unique_times = sorted(df_stat["commit_time"].unique().tolist())
            self._print_time_bar(None, unique_times, df_stat, bar_divider=200)

        return df_stat
