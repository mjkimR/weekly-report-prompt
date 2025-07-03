# schemas.py

from datetime import datetime
from pydantic import BaseModel


class CommitStats(BaseModel):
    insertions: int
    deletions: int
    files: int


class CommitData(BaseModel):
    id: str
    author: str
    email: str
    date: datetime
    message: str
    stats: CommitStats
    diff: str

    @classmethod
    def from_commit(cls, commit, diff):
        """커밋 객체로부터 CommitData 인스턴스 생성"""
        return cls(
            id=commit.hexsha,
            author=commit.author.name,
            email=commit.author.email,
            date=commit.committed_datetime.isoformat(),
            message=commit.message.strip(),
            stats=CommitStats(
                insertions=commit.stats.total["insertions"],
                deletions=commit.stats.total["deletions"],
                files=commit.stats.total["files"],
            ),
            diff=diff,
        )


class CommitDataSummary(BaseModel):
    start_date: datetime
    end_date: datetime

    total_commits: int
    total_insertions: int
    total_deletions: int
    total_files_changed: int
