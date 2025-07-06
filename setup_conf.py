import os
import shutil
from pathlib import Path

from weekly_report_prompt.const import MEMO_BLANK_MESSAGE

repo_dir = str(Path(__file__).parent)


def copy_config_example():
    os.makedirs(os.path.join(repo_dir, "config"), exist_ok=True)
    for src, tgt in [
        ("config.yaml.example", "config.yaml"),
        ("template.md.example", "template.md"),
    ]:
        src = os.path.join(repo_dir, "config", src)
        dst = os.path.join(repo_dir, "config", tgt)

        if not os.path.exists(dst):
            shutil.copyfile(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"{dst} already exists. Skipping copy.")


def create_memo_md():
    memo_path = os.path.join(repo_dir, "build", "memo.md")
    os.makedirs(os.path.dirname(memo_path), exist_ok=True)
    if os.path.exists(memo_path):
        print(f"{memo_path} already exists. Skipping creation.")
        return
    with open(memo_path, "w", encoding="utf-8") as f:
        f.write(MEMO_BLANK_MESSAGE)
    print(f"Created {memo_path}")


if __name__ == "__main__":
    copy_config_example()
    create_memo_md()
