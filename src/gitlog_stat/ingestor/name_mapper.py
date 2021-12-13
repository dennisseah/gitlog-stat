"""Name mapper."""

mapper = {
    "Smutnuri": "Satya Mutnuri",
    "Veseah": "Dennis Seah",
}


class NameMapper:
    """This class is responsible for mapping names."""

    @staticmethod
    def map(name: str):
        """Return mapped name otherwise name will be returned.

        Args:
            name (str): name for mapping.

        Returns:
            str: mapped name.
        """
        return mapper[name] if name in mapper else name
