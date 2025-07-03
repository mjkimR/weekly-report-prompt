from typing import List, Optional, Dict, Any
from schemas import CommitData, CommitDataSummary


class PromptGenerator:
    def __init__(
            self,
            project_data: List[Dict[str, Any]],
            config_loader,
    ):
        """
        Args:
            project_data: 프로젝트별 데이터 리스트 (각 dict에 project_name, recent_commits, summary, previous_report 등 포함)
            config_loader: 설정 로더 인스턴스
        """
        self.project_data = project_data
        self.config_loader = config_loader
        self.max_diff_lines = config_loader.get_max_diff_lines()
        self.lang = config_loader.get_lang()

    def _format_commit(self, commit: CommitData, include_diff: bool) -> str:
        """단일 커밋 정보를 문자열로 포맷합니다."""
        commit_lines = []
        # 커밋 메시지 (첫 줄만 사용하거나, 전체를 사용하거나 선택 가능. 여기서는 전체 사용)
        # 메시지가 여러 줄일 경우를 대비해 첫 줄만 강조하거나, 적���히 요약하는 로직 추가 가능
        commit_message_lines = commit.message.strip().split("\n")
        formatted_message = (
            f"- **{commit_message_lines[0].strip()}**"  # 첫 줄은 Bold 처리
        )
        if len(commit_message_lines) > 1:
            formatted_message += "\n  " + "\n  ".join(commit_message_lines[1:])

        commit_lines.append(
            f"{formatted_message} (ID: {commit.id[:7]}, Date: {commit.date.strftime('%Y-%m-%d')})"
        )

        if include_diff and commit.diff:
            diff_content_lines = commit.diff.strip().splitlines()
            if len(diff_content_lines) > self.max_diff_lines:
                diff_display = "\n".join(
                    [
                        f"    {line}"
                        for line in diff_content_lines[: self.max_diff_lines]
                    ]
                )
                diff_display += f"\n    ... (Diff 내용 일부 생략, 총 {len(diff_content_lines)} 줄 중 {self.max_diff_lines} 줄 표시)"
            else:
                diff_display = "\n".join([f"    {line}" for line in diff_content_lines])

            commit_lines.append(f"  ```diff\n{diff_display}\n  ```")
        return "\n".join(commit_lines)

    def _format_commits(
            self, commits: List[CommitData], should_include_diff=True
    ) -> str:
        """커밋 리스트를 문자열로 포맷합니다."""
        if not commits:
            return "  - 해당 사항 없음"

        formatted_commits_text = [
            self._format_commit(commit, include_diff=should_include_diff)
            for commit in commits
        ]
        return "\n".join(formatted_commits_text)

    def generate_prompt(self, should_include_diff=True) -> str:
        if self.lang == "en":
            prompt_sections = [
                "# Weekly Work Report Request",
                "Hello! Please draft a weekly work report based on the provided Git activity and previous report (if available).",
            ]
        else:
            prompt_sections = [
                "# 주간 업무 보고서 생성 요청",
                "안녕하세요! 제공된 Git 활동 내역과 이전 보고서(해당하는 경우)를 바탕으로 주간 업무 보고서 ���안을 작성해 주세요.",
            ]

        # --- 프로젝��별 섹션 ---
        for project in self.project_data:
            project_name = project["project_name"]
            summary = project["summary"]
            previous_report = project.get("previous_report")
            recent_commits = project["recent_commits"]

            # 이전 보고서
            if previous_report and previous_report.strip():
                previous_report_section = [
                    f"## 📝 [{project_name}] 이전 주간 보고서 (참고용)",
                    "이전 보고서의 내용과 스타일을 참고하여 일관성을 유지하고, 중복되는 내용은 피해주세요.",
                    "```text",
                    previous_report.strip(),
                    "```",
                ]
                prompt_sections.append("\n".join(previous_report_section))

            # 요약
            summary_title = f"## 📊 [{project_name}] 금주 Git 활동 요약"
            summary_content = []
            if summary:
                summary_content.append(
                    f"{summary_title} ({summary.start_date.strftime('%Y-%m-%d')} ~ {summary.end_date.strftime('%Y-%m-%d')})"
                )
                summary_content.append(f"- 총 커밋: {summary.total_commits}건")
                summary_content.append(f"- 총 추가된 라인: {summary.total_insertions}줄")
                summary_content.append(f"- 총 삭제된 라인: {summary.total_deletions}줄")
                summary_content.append(f"- 변경된 파일 수: {summary.total_files_changed}개")
            else:
                summary_content.append(summary_title)
                summary_content.append("- 해당 기간 동안의 Git 활동 요약 정보가 없습니다.")
            prompt_sections.append("\n".join(summary_content))

            # 커밋 상세
            commit_details_header = f"## 🚀 [{project_name}] 금주 주요 진행 사항 (Git 커밋 기반)"
            commit_details_parts = [
                commit_details_header,
                self._format_commits(recent_commits, should_include_diff),
            ]
            prompt_sections.append("\n".join(commit_details_parts))

        # --- 보고서 작성 지침 ---
        instructions = [
            "\n## 📄 보고서 작성 지침",
            "\n**보고서 스타일 및 주의사항:**",
            "- 각 프로젝트별로 섹션을 구분하여 작성해 주세요.",
            "- 각 항목은 명확하고 간결하게 작성해 주세요. 불필요한 중복이나 모호한 표현은 피해주세요.",
            "- 형식이 이전 주간 보고서와 일치하도록, 각 항목은 제목과 내용을 구분하여 작성해 주세요.",
            "- 커밋 메시지와 코드 변경 사항을 바탕으로 작성하되, 필요한 경우 추가적인 설명을 통해 맥락을 보완해 주세요.",
            "- 명확하고 간결하며, 이해하기 쉬운 전문적인 어투를 사용해 주세요.",
        ]
        prompt_sections.append("\n".join(instructions))

        return "\n\n".join(prompt_sections)
