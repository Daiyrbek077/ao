from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MediaSet:
    img_question: Optional[str] = None
    img_answer: Optional[str] = None
    video_question: Optional[str] = None
    video_answer: Optional[str] = None
    audio_question: Optional[str] = None
    audio_answer: Optional[str] = None


@dataclass
class Question:
    category: str
    score: int
    question: str
    answer: str
    timer: str
    media: MediaSet = field(default_factory=MediaSet)


@dataclass
class BonusQuestion:
    category: str
    score: int
    type: str


@dataclass
class GameData:
    title: str
    bonusQuestions: Dict[str, BonusQuestion] = field(default_factory=dict)
    questions: List[Question] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "bonusQuestions": {
                name: {
                    "category": bonus.category,
                    "score": bonus.score,
                    "type": bonus.type,
                }
                for name, bonus in self.bonusQuestions.items()
            },
            "questions": [
                {
                    "category": question.category,
                    "score": question.score,
                    "question": question.question,
                    "answer": question.answer,
                    "timer": question.timer,
                    "media": {
                        "img_question": question.media.img_question,
                        "img_answer": question.media.img_answer,
                        "video_question": question.media.video_question,
                        "video_answer": question.media.video_answer,
                        "audio_question": question.media.audio_question,
                        "audio_answer": question.media.audio_answer,
                    },
                }
                for question in self.questions
            ],
        }

    @staticmethod
    def from_dict(payload: dict) -> "GameData":
        bonus = {
            name: BonusQuestion(
                category=data["category"],
                score=int(data["score"]),
                type=data["type"],
            )
            for name, data in payload.get("bonusQuestions", {}).items()
        }
        questions = []
        for item in payload.get("questions", []):
            media_payload = item.get("media", {})
            media = MediaSet(
                img_question=media_payload.get("img_question"),
                img_answer=media_payload.get("img_answer"),
                video_question=media_payload.get("video_question"),
                video_answer=media_payload.get("video_answer"),
                audio_question=media_payload.get("audio_question"),
                audio_answer=media_payload.get("audio_answer"),
            )
            questions.append(
                Question(
                    category=item["category"],
                    score=int(item["score"]),
                    question=item["question"],
                    answer=item["answer"],
                    timer=item.get("timer", "auto"),
                    media=media,
                )
            )
        return GameData(title=payload["title"], bonusQuestions=bonus, questions=questions)
