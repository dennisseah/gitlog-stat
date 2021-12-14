"""All Git Commit by Day Report Generator."""

from gitlog_stat.reports.report_base import ReportBase


class AllCommitByDay(ReportBase):
    """All Git Commit by Day Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        df_commit_by_day = (
            df[["commit_day", "lines_total"]]
            .groupby(["commit_day"])["lines_total"]
            .sum()
            .reset_index()
        )

        if print_rpt:
            unique_days = self._unique_days(df_commit_by_day)
            self._print_day_bar(None, unique_days, df_commit_by_day, bar_divider=500)

        return df_commit_by_day
