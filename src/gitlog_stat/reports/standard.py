"""Standard Report Generator."""
import pandas as pd
from tabulate import tabulate

from gitlog_stat.reports.report_base import ReportBase


class Standard(ReportBase):
    """Standard Report Generator."""

    def build(self, df, print_rpt=False):
        """Build a report.

        Args:
            df (DataFrame): DataFrame with raw data
            print_rpt (boolean): True to print report

        Returns:
            [type]: [description]
        """
        df_titles = (
            df[["author", "title", "is_customer"]]
            .drop_duplicates(["author", "title", "is_customer"])
            .reset_index(drop=True)
        )
        df_titles.loc[(df_titles["is_customer"]), "title"] = "Customer"

        df_commit_time_min = (
            df[["author", "commit_ts"]].groupby("author")["commit_ts"].min().reset_index()
        )
        df_commit_time_min.rename(columns={"commit_ts": "min_commit_time"}, inplace=True)
        df_commit_time_min["min_commit_time"] = df_commit_time_min["min_commit_time"].dt.strftime(
            "%Y-%m-%d"
        )

        df_commit_time_max = (
            df[["author", "commit_ts"]].groupby("author")["commit_ts"].max().reset_index()
        )
        df_commit_time_max.rename(columns={"commit_ts": "max_commit_time"}, inplace=True)
        df_commit_time_max["max_commit_time"] = df_commit_time_max["max_commit_time"].dt.strftime(
            "%Y-%m-%d"
        )

        df_files_changed = (
            df[["author", "files_changed"]].groupby("author")["files_changed"].sum().reset_index()
        )
        df_lines_added = (
            df[["author", "lines_added"]].groupby("author")["lines_added"].sum().reset_index()
        )

        df_lines_deleted = (
            df[["author", "lines_deleted"]].groupby("author")["lines_deleted"].sum().reset_index()
        )

        df_stat = df_titles

        for d in [
            df_commit_time_min,
            df_commit_time_max,
            df_files_changed,
            df_lines_added,
            df_lines_deleted,
        ]:
            df_stat = pd.merge(df_stat, d, on="author", how="inner").reset_index(drop=True)

        col_exts = sorted(filter(lambda x: x.startswith("ext_"), df.columns.to_list()))

        for ext in col_exts:
            df_ext = df[["author", ext]].groupby("author")[ext].sum().reset_index()
            df_stat = pd.merge(df_stat, df_ext, on="author", how="inner")

        if print_rpt:
            self.print_report(df_stat)

        return df_stat

    def print_report(self, df_stat):
        """Print report.

        Args:
            df_stat (DataFrame): statistic dataframe.
        """
        self._print_std_report(df_stat)
        self._print_file_ext_report(df_stat)

    def _print_file_ext_report(self, df_stat):
        cols_extensions = list(filter(lambda x: x.startswith("ext_"), df_stat.columns.to_list()))
        extensions = list(map(lambda x: x[4:], cols_extensions))

        self._print_title("By File Types (number of files touched)")
        df = df_stat[
            [
                "author",
                "title",
            ]
            + cols_extensions
        ].copy(deep=True)
        df.sort_values(by=["author"], axis=0, inplace=True)

        print(
            tabulate(df, headers=["author", "role"] + extensions, showindex=False).replace(
                " 0", " -"
            )
        )
        print()

    def _print_std_report(self, df_stat):
        headers = [
            "Engineer",
            "Role",
            "Begin Contrib.",
            "Last Contrib.",
            "File Touched",
            "Lines (+)",
            "Lines (-)",
        ]

        self._print_title("General Information")
        df = df_stat[
            [
                "author",
                "title",
                "min_commit_time",
                "max_commit_time",
                "files_changed",
                "lines_added",
                "lines_deleted",
            ]
        ].copy(deep=True)
        df.sort_values(by=["author"], axis=0, inplace=True)
        print(tabulate(df, headers=headers, showindex=False))
        print()
