from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from infrasentinel_ai.schemas import RetrievalResult


@dataclass(frozen=True)
class Playbook:
    title: str
    text: str


class PlaybookRetriever:
    def __init__(self, playbooks: list[Playbook]) -> None:
        self.playbooks = playbooks
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([playbook.text for playbook in playbooks])

    @classmethod
    def from_markdown(cls, path: Path) -> "PlaybookRetriever":
        text = path.read_text(encoding="utf-8")
        playbooks: list[Playbook] = []
        for raw_section in text.split("\n## "):
            section = raw_section.strip()
            if not section:
                continue
            lines = section.splitlines()
            title = lines[0].replace("#", "").strip()
            body = "\n".join(lines[1:]).strip()
            playbooks.append(Playbook(title=title, text=body or title))
        return cls(playbooks)

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        ranked = scores.argsort()[::-1][:top_k]
        return [
            RetrievalResult(
                title=self.playbooks[index].title,
                score=round(float(scores[index]), 4),
                text=self.playbooks[index].text,
            )
            for index in ranked
        ]
