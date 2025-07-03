from git_data_collector import GitDataCollector
from prompt_generator import PromptGenerator
from schemas import CommitDataSummary
from datetime import datetime
from config_loader import ConfigLoader


def summarize_commit_data(commits):
    """Git 데이터 요약 정보 생성"""
    return CommitDataSummary(
        start_date=min([commit.date for commit in commits], default=datetime.now()),
        end_date=max([commit.date for commit in commits], default=datetime.now()),
        total_commits=len(commits),
        total_insertions=sum(commit.stats.insertions for commit in commits),
        total_deletions=sum(commit.stats.deletions for commit in commits),
        total_files_changed=sum(commit.stats.files for commit in commits),
    )


# ConfigLoader 인스턴스 생성 및 설정값 로드
def main():
    config = ConfigLoader()
    repo_paths = config.get_repositories()

    project_data = []
    for repo_path in repo_paths:
        project_name = repo_path.rstrip("/").split("/")[-1]  # 폴더명으로 프로젝트명 추정
        collector = GitDataCollector(
            config_loader=config, repo_path=repo_path
        )
        recent_commits = collector.collect_commits(days=7)
        summary_data = summarize_commit_data(recent_commits)
        previous_report_content = None
        try:
            with open(f"../previous/{project_name}_prev.md", "r", encoding="utf-8") as f:
                previous_report_content = f.read()
        except FileNotFoundError:
            pass
        project_data.append({
            "project_name": project_name,
            "repo_path": repo_path,
            "recent_commits": recent_commits,
            "summary": summary_data,
            "previous_report": previous_report_content,
        })

    if not project_data or all(len(p["recent_commits"]) == 0 for p in project_data):
        raise ValueError("최근 7일간 커밋이 없습니다. 작성자를 확인하거나 기간을 조정해 주세요.")

    prompt_gen = PromptGenerator(
        project_data=project_data,
        config_loader=config,
        lang=lang
    )
    final_prompt_for_llm = prompt_gen.generate_prompt()
    print(final_prompt_for_llm)


if __name__ == "__main__":
    main()
