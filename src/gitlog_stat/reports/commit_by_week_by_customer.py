"""Git Commit by Week by Customer Report Generator."""

import numpy as np
from gitlog_stat.reports.report_base import ReportBase


class CommitByWeekByCustomer(ReportBase):
    """Git Commit by Week by Customer Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        df_commit_per_week = (
            df[["is_customer", "week_of_year", "lines_total"]]
            .groupby(["is_customer", "week_of_year"])["lines_total"]
            .sum()
            .reset_index()
        )

        df_commit_per_week["author"] = np.where(df_commit_per_week.is_customer, "Customer", "CSE")

        if print_rpt:
            self.print_report(df_commit_per_week)

        return df_commit_per_week

    def print_report(self, df_stat):
        """Print report.

        Args:
            df_stat (DataFrame): statistic dataframe.
        """
        unique_weeks = sorted(df_stat["week_of_year"].unique().tolist())
        for author in df_stat["author"].unique().tolist():
            self._print_week_bar(author, unique_weeks, df_stat)
