"""Log entry."""

import pandas as pd

TABU_EXT = [
    "cfg",
    "cmd",
    "csproj",
    "dockerignore",
    "editorconfig",
    "env",
    "feature",
    "gitattributes",
    "gitignore",
    "http",
    "mod",
    "refactorlog",
    "ruleset",
    "runconfig",
    "sln",
    "sqlproj",
    "sum",
    "targets",
    "flake8",
    "msapp",
]

EXT_MAP = {
    "yaml": "yml",
    "png": "images",
    "jpeg": "images",
    "jpg": "images",
    "drawio": "images",
    "vsdx": "images",
    "mp4": "videos",
    "tfvars": "tf",
    "csv": "data",
    "dsv": "data",
    "parquet": "data",
}


class LogEntry:
    """Log entry."""

    def __init__(self, block):
        """Instantiate an instance of this class.

        Args:
            block (Block): block of raw log data
        """
        self.author = block.author()
        self.email = block.email()
        self.is_customer = block.is_customer()
        self.commit_time = block.commit_time()

        stat = block.commit_stat()
        self.files_changed = stat["files_changed"]
        self.lines_added = stat["lines_added"]
        self.lines_deleted = stat["lines_deleted"]

        self.file_touched = [] + block.files_touched()

    def file_touched_ext(self):
        """Extensions of file touched."""
        results = {}

        for f in self.file_touched:
            try:
                lastindex = f.rindex(".")
                ext = f[lastindex + 1 :]
                if ext[-1] == "}":
                    ext = ext[0, -1]

                if ext not in TABU_EXT and "/" not in ext:
                    if ext in EXT_MAP:
                        ext = EXT_MAP[ext]
                    if ext not in results:
                        results[ext] = 0
                    results[ext] += 1

            except Exception:
                pass

        return results

    @staticmethod
    def all_extensions(entries):
        """All unique extensions.

        Args:
            entries (LogEntry): list of log entries

        Returns:
            [Set]: Set of extensions.
        """
        results = set()

        for entry in entries:
            extensions = entry.file_touched_ext()
            for e in extensions:
                results.add(e)
        return results

    @staticmethod
    def to_dataframe(entries):
        """Create pandas dataframe from data.

        Args:
            entries (LogEntry): list of log entries
        """
        data = {
            "author": [],
            "email": [],
            "is_customer": [],
            "commit_time": [],
            "files_changed": [],
            "lines_added": [],
            "lines_deleted": [],
            "file_touched": [],
        }

        extensions = LogEntry.all_extensions(entries)
        # print(extensions)
        for e in extensions:
            data["ext_" + e] = []

        for entry in entries:
            exts = entry.file_touched_ext()
            for e in extensions:
                data["ext_" + e].append(exts[e] if e in exts else 0)

            if entry.is_customer:
                data["author"].append(entry.author + " (*)")
            else:
                data["author"].append(entry.author)
            data["email"].append(entry.email)
            data["is_customer"].append(entry.is_customer)
            data["commit_time"].append(entry.commit_time)
            data["files_changed"].append(entry.files_changed)
            data["lines_added"].append(entry.lines_added)
            data["lines_deleted"].append(entry.lines_deleted)
            data["file_touched"].append(",".join(entry.file_touched))

        df = pd.DataFrame.from_dict(data)

        df["commit_ts"] = pd.to_datetime(df["commit_time"])
        df["commit_time"] = df["commit_ts"].dt.round("H").dt.hour
        df["commit_day"] = df["commit_ts"].dt.day_name()

        df["week_of_year"] = (
            df["commit_ts"].dt.year.astype(str)
            + "_"
            + df["commit_ts"]
            .dt.isocalendar()
            .week.astype(str)
            .str.pad(2, side="left", fillchar="0")
        )
        df["lines_total"] = df["lines_added"] + df["lines_deleted"]

        return df
