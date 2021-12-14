"""Report base class."""


BAR_SYMBOL = "#"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class ReportBase:
    """Report base class."""

    def _gen_report(
        self, df_stat, author, title, dimensions, measure, dim_prefix=None, bar_divider=50
    ):
        print()
        self._print_title(title)
        df = df_stat[df_stat.author == author].reset_index() if author else df_stat

        data = {}
        raw_data = df.to_dict()
        for idx in raw_data[measure]:
            data[raw_data[measure][idx]] = raw_data["lines_total"][idx]

        for d in dimensions:
            val = data[d] if d in data else ""
            bar = min(ReportBase.__roundup(val / bar_divider), 100) if val else 0
            val = str(val).rjust(6) if val else ".".rjust(6)
            dim = str(d) + dim_prefix if dim_prefix else str(d)

            print(
                "{dim:10s} | {val} {bar}".format(dim=dim.rjust(10), val=val, bar=BAR_SYMBOL * bar)
            )

        print()

    def _print_week_bar(self, author: str, unique_weeks: list, df_stat):
        """Print week activities bar chart.

        Args:
            author (str): Author name
            unique_weeks (list): list of unique weeks (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        self._gen_report(
            df_stat,
            author,
            "{} - lines of code changed per week".format(author),
            unique_weeks,
            "week_of_year",
        )

    def _print_day_bar(self, author: str, unique_days: list, df_stat, bar_divider=50):
        """Print day activities bar chart.

        Args:
            author (str): Author name
            unique_days (list): list of unique days (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        self._gen_report(
            df_stat,
            author,
            "{} - lines of code changed by day".format(author if author else "All"),
            unique_days,
            "commit_day",
            bar_divider=bar_divider,
        )

    def _print_time_bar(self, author: str, unique_times: list, df_stat):
        """Print time activities bar chart.

        Args:
            author (str): Author name
            unique_times (list): list of unique times (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        self._gen_report(
            df_stat,
            author,
            "{} - lines of code changed by time".format(author),
            unique_times,
            "commit_time",
            ":00",
        )

    @staticmethod
    def __roundup(number):
        return round(number + 0.5)

    def _print_title(self, title: str):
        print("\n\n" + title + "\n")

    def _unique_days(self, df_stat):
        return sorted(df_stat["commit_day"].unique().tolist(), key=DAYS.index)
