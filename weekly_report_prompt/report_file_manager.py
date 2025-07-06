import os
import re
from datetime import datetime
from pathlib import Path

from config_loader import ConfigLoader
from const import REPORT_BLANK_MESSAGE, MEMO_BLANK_MESSAGE


class ReportFileManager:
    def __init__(self, config_loader: ConfigLoader, build_dir=None):
        if build_dir is None:
            build_dir = os.path.join(Path(__file__).parent.parent, "build")
            if not os.path.isdir(build_dir):
                # Create the default build directory if it does not exist
                os.makedirs(build_dir, exist_ok=True)
        if not os.path.isdir(build_dir):
            raise NotADirectoryError(f"Build directory does not exist: {build_dir}")
        self.build_dir = build_dir
        self.history_dir = os.path.join(self.build_dir, "history")
        os.makedirs(self.history_dir, exist_ok=True)

        self.history_limit = config_loader.get_report_history_limit()
        self.prompt_file_path = None

    def get_today_str(self):
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def save_prompt(self, prompt_text):
        filename = f"prompt-{self.get_today_str()}.md"
        path = os.path.join(self.build_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        self.prompt_file_path = path
        return path

    def create_report_file(self):
        filename = f"report-{self.get_today_str()}.md"
        path = os.path.join(self.build_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(REPORT_BLANK_MESSAGE)
        return path

    def move_previous_reports(self):
        """Move previous reports to the history directory."""
        for filename in os.listdir(self.build_dir):
            if filename.startswith("report-") and filename.endswith(".md"):
                file_path = os.path.join(self.build_dir, filename)
                # Check file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if content.strip() != REPORT_BLANK_MESSAGE.strip():
                    # Move to history directory
                    dest_path = os.path.join(self.history_dir, filename)
                    os.rename(file_path, dest_path)
                else:
                    # If the report is blank, delete it
                    os.remove(file_path)

    def fetch_report_history(self):
        """Return a list of previous reports."""
        reports = []
        for filename in os.listdir(self.history_dir):
            if filename.startswith("report-") and filename.endswith(".md"):
                with open(
                        os.path.join(self.history_dir, filename), "r", encoding="utf-8"
                ) as f:
                    content = f.read()
                reports.append(content)
        return sorted(reports, reverse=True)[: self.history_limit]

    def get_last_report_date(self):
        """Return the date of the last report."""
        dates = []
        for filename in os.listdir(self.history_dir):
            match = re.match(r"report-(\d{8}-\d{6})\.md", filename)
            if match:
                date_str = match.group(1)
                date = datetime.strptime(date_str, "%Y%m%d-%H%M%S")
                dates.append(date)
        return max(dates) if dates else None

    def clear_previous_prompts(self):
        """Clear all previous prompt files."""
        for filename in os.listdir(self.build_dir):
            if filename.startswith("prompt-") and filename.endswith(".md"):
                file_path = os.path.join(self.build_dir, filename)
                os.remove(file_path)

    def fetch_memo(self):
        memo_path = os.path.join(self.build_dir, "memo.md")
        if not os.path.exists(memo_path):
            with open(memo_path) as f:
                f.write(MEMO_BLANK_MESSAGE)
        with open(os.path.join(self.build_dir, "memo.md"), "r", encoding="utf-8") as f:
            memo = f.read().strip()
        if memo == MEMO_BLANK_MESSAGE.strip():
            return None
        return memo
