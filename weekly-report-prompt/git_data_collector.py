# git_data_collector.py

import git
from datetime import datetime, timedelta
from typing import List, Optional

from schemas import CommitData


class GitDataCollector:
    def __init__(self, config_loader, repo_path: str = "."):
        self.config_loader = config_loader
        self.author = config_loader.get_author()
        self.repo = git.Repo(repo_path)

    def collect_commits(
            self,
            days: int = 7,
            target_date: Optional[datetime] = None
    ) -> List[CommitData]:
        if target_date is None:
            target_date = datetime.now()
        since_date = target_date - timedelta(days=days)

        commits = []
        for commit in self.repo.iter_commits(since=since_date):
            # merge commit 제외
            if len(commit.parents) > 1:
                continue
            # 작성자가 일치하지 않는 커밋 제외
            if commit.author.name != self.author:
                continue

            commit_data = CommitData.from_commit(commit, self.get_commit_diff(commit.hexsha))
            commits.append(commit_data)

        return commits

    def get_commit_diff(self, commit_id: str) -> str:
        """특정 커밋의 diff 정보 반환"""
        commit = self.repo.commit(commit_id)
        if len(commit.parents) > 0:
            return self.repo.git.diff(commit.parents[0], commit)
        else:
            return self.repo.git.diff(git.NULL_TREE, commit)
