from pathlib import Path

from infrasentinel_ai.rag.playbooks import PlaybookRetriever


def test_playbook_retriever_returns_relevant_result(tmp_path: Path) -> None:
    playbooks = tmp_path / "playbooks.md"
    playbooks.write_text(
        "# Playbooks\n\n"
        "## SSH Investigation\nReview failed SSH attempts.\n\n"
        "## Data Exfiltration\nInspect outbound data volume.\n",
        encoding="utf-8",
    )
    retriever = PlaybookRetriever.from_markdown(playbooks)

    result = retriever.search("failed SSH login", top_k=1)[0]

    assert result.title == "SSH Investigation"
    assert result.score > 0
