"""Log ingestor."""

from gitlog_stat.ingestor.block import Block


class Ingestor:
    """This class provides a few way to gather git log raw data."""

    @staticmethod
    def ingest_from_file(file_paths: list):
        """Ingest log from file.

        Args:
            file_paths (list): list of file paths.
        """
        buff = ""
        for p in file_paths:
            with open(p) as f:
                buff += f.read()
        return Block.parse(buff)
