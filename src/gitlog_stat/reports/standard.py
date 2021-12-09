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
        df_commit_time_min = (
            df[["author", "commit_time"]].groupby("author")["commit_time"].min().reset_index()
        )
        df_commit_time_min.rename(columns={"commit_time": "min_commit_time"}, inplace=True)
        df_commit_time_min["min_commit_time"] = df_commit_time_min["min_commit_time"].dt.strftime(
            "%Y-%m-%d"
        )

        df_commit_time_max = (
            df[["author", "commit_time"]].groupby("author")["commit_time"].max().reset_index()
        )
        df_commit_time_max.rename(columns={"commit_time": "max_commit_time"}, inplace=True)
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

        df_stat = df_commit_time_min

        for d in [df_commit_time_max, df_files_changed, df_lines_added, df_lines_deleted]:
            df_stat = pd.merge(df_stat, d, on="author", how="inner")

        for ext in filter(lambda x: x.startswith("ext_"), df.columns.to_list()):
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
        print(
            tabulate(
                df_stat[
                    [
                        "author",
                    ]
                    + cols_extensions
                ],
                headers=["author"] + extensions,
                showindex=False,
            ).replace(" 0", " -")
        )
        print()

    def _print_std_report(self, df_stat):
        headers = [
            "Engineer",
            "Begin Contrib.",
            "Last Contrib.",
            "File Touched",
            "Lines (+)",
            "Lines (-)",
        ]

        self._print_title("General Information ( * - Customer)")
        print(
            tabulate(
                df_stat[
                    [
                        "author",
                        "min_commit_time",
                        "max_commit_time",
                        "files_changed",
                        "lines_added",
                        "lines_deleted",
                    ]
                ],
                headers=headers,
                showindex=False,
            )
        )
        print()
