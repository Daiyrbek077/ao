from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass
class Media:
    img_question: Optional[str] = None
    img_answer: Optional[str] = None
    video_question: Optional[str] = None
    video_answer: Optional[str] = None
    audio_question: Optional[str] = None
    audio_answer: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "img_question": self.img_question,
            "img_answer": self.img_answer,
            "video_question": self.video_question,
            "video_answer": self.video_answer,
            "audio_question": self.audio_question,
            "audio_answer": self.audio_answer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Media":
        return cls(
            img_question=data.get("img_question"),
            img_answer=data.get("img_answer"),
            video_question=data.get("video_question"),
            video_answer=data.get("video_answer"),
            audio_question=data.get("audio_question"),
            audio_answer=data.get("audio_answer"),
        )


@dataclass
class Question:
    category: str
    score: int
    question: str
    answer: str
    timer: str
    media: Media = field(default_factory=Media)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "score": self.score,
            "question": self.question,
            "answer": self.answer,
            "timer": self.timer,
            "media": self.media.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        return cls(
            category=data["category"],
            score=int(data["score"]),
            question=data["question"],
            answer=data["answer"],
            timer=data.get("timer", "auto"),
            media=Media.from_dict(data.get("media", {})),
        )


@dataclass
class GameData:
    title: str
    bonus_questions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    questions: List[Question] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "bonusQuestions": self.bonus_questions,
            "questions": [question.to_dict() for question in self.questions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameData":
        questions = [Question.from_dict(item) for item in data.get("questions", [])]
        return cls(
            title=data.get("title", "Untitled"),
            bonus_questions=data.get("bonusQuestions", {}),
            questions=questions,
        )

    @classmethod
    def load(cls, path: Path) -> "GameData":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)

    def save(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)
