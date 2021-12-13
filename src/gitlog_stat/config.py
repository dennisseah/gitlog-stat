"""Configuration file parser."""

import json
import os


CONFIG_FILE_NAME = "gitlogstat.json"


class Config:
    """Configuration class."""

    company_email_domains = []
    employee_emails = []
    excluded_extensions = []
    extension_mappings = {}

    @classmethod
    def _parse(cls):
        cur_path = os.path.abspath(os.getcwd())
        cfg_path = None

        while cur_path != os.path.sep and cfg_path is None:
            test_path = os.path.join(cur_path, CONFIG_FILE_NAME)

            if os.path.exists(test_path):
                cfg_path = test_path
            else:
                cur_path = os.path.dirname(cur_path)

        if cfg_path:
            with open(cfg_path) as f:
                return json.loads(f.read())

        return None

    @classmethod
    def parse(cls):
        """Parse configuration file."""
        cfg = cls._parse()
        cls.employee_emails = cfg.get("employee-emails", [])
        cls.company_email_domains = cfg.get("company-email-domains", [])
        cls.excluded_extensions = cfg.get("excluded-extensions", [])
        cls.extension_mappings = cfg.get("extension-mappings", {})
