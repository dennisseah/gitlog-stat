"""Report base class."""


class ReportBase:
    """Report base class."""

    def _print_week_bar(self, author: str, unique_weeks: list, df_stat):
        """Print week activities bar chart.

        Args:
            author (str): Author name
            unique_weeks (list): list of unique weeks (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        print()
        self._print_title("{} - lines of code changed per week".format(author))
        df = df_stat[df_stat.author == author].reset_index()

        data = {}
        raw_data = df.to_dict()
        for idx in raw_data["week_of_year"]:
            data[raw_data["week_of_year"][idx]] = raw_data["lines_total"][idx]

        for w in unique_weeks:
            val = data[w] if w in data else ""
            bar = min(ReportBase.__roundup(val / 50), 100) if val else 0
            val = str(val).rjust(5) if val else ".".rjust(5)

            print("{wk} | {val} {bar}".format(wk=w, val=val, bar="#" * bar))

        print()

    def _print_day_bar(self, author: str, unique_days: list, df_stat):
        """Print day activities bar chart.

        Args:
            author (str): Author name
            unique_days (list): list of unique days (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        print()
        self._print_title("{} - lines of code changed by day".format(author))
        df = df_stat[df_stat.author == author].reset_index()

        data = {}
        raw_data = df.to_dict()
        for idx in raw_data["commit_day"]:
            data[raw_data["commit_day"][idx]] = raw_data["lines_total"][idx]

        for d in unique_days:
            val = data[d] if d in data else ""
            bar = min(ReportBase.__roundup(val / 50), 100) if val else 0
            val = str(val).rjust(5) if val else ".".rjust(5)

            print("{day:9s} | {val} {bar}".format(day=d, val=val, bar="#" * bar))

        print()

    def _print_time_bar(self, author: str, unique_times: list, df_stat):
        """Print time activities bar chart.

        Args:
            author (str): Author name
            unique_times (list): list of unique times (string)
            df_stat (DataFrame): raw statistic dataframe.
        """
        print()
        self._print_title("{} - lines of code changed by time".format(author))
        df = df_stat[df_stat.author == author].reset_index()

        data = {}
        raw_data = df.to_dict()
        for idx in raw_data["commit_time"]:
            data[raw_data["commit_time"][idx]] = raw_data["lines_total"][idx]

        for tm in unique_times:
            val = data[tm] if tm in data else ""
            bar = min(ReportBase.__roundup(val / 50), 100) if val else 0
            val = str(val).rjust(5) if val else ".".rjust(5)

            print("{time:2d} hours | {val} {bar}".format(time=tm, val=val, bar="#" * bar))

        print()

    @staticmethod
    def __roundup(number):
        return round(number + 0.5)

    def _print_title(self, title: str):
        print("\n\n" + title + "\n")
