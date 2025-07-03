import os
from datetime import datetime
from pathlib import Path


class ReportFileManager:
    def __init__(self, build_dir=None, history_limit=10):
        if build_dir is None:
            build_dir = os.path.join(Path(__file__).parent.parent, "build")
            if not os.path.isdir(build_dir):
                # 기본 빌드 디렉토리가 없으면 생성
                os.makedirs(build_dir, exist_ok=True)
        if not os.path.isdir(build_dir):
            raise NotADirectoryError(f"빌드 디렉토리가 존재하지 않습니다: {build_dir}")
        self.build_dir = build_dir
        self.history_dir = os.path.join(self.build_dir, "history")
        os.makedirs(self.history_dir, exist_ok=True)

        self.history_limit = history_limit

    def get_today_str(self):
        return datetime.now().strftime("%Y-%m-%d")

    def save_prompt(self, prompt_text):
        filename = f"prompt-{self.get_today_str()}.md"
        path = os.path.join(self.build_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        return path

    def create_report_file(self):
        filename = f"report-{self.get_today_str()}.md"
        path = os.path.join(self.build_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("# 여기에 LLM으로 생성한 리포트 결과를 붙여넣기 한 다음 최종 수정하세요\n")
        return path
