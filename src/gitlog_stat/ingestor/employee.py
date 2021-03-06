"""Determine if an email belongs to Microsoft employee."""

from gitlog_stat.config import Config


class Employee:
    """This class is responsibility for figuring out if an email belongs to Microsoft employee."""

    @staticmethod
    def is_employee(email: str):
        """Return True if email belongs to Microsoft employee.

        Args:
            email (str): email address

        Returns:
            bool: True if email belongs to Microsoft employee.
        """
        return email.lower() in Config.employee_emails
