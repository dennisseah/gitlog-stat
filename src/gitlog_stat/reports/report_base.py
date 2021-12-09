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
            val = data[w] if w in data else 0
            bar = min(ReportBase.__roundup(val / 50), 100)

            print("{wk} | {val:6.0f} {bar}".format(wk=w, val=val, bar="#" * bar))

        print()

    @staticmethod
    def __roundup(number):
        return round(number + 0.5)

    def _print_title(self, title: str):
        print("\n\n" + title + "\n")
