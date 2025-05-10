from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    description: Mapped[str] = mapped_column(db.String, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"), nullable=True)
    goal = relationship("Goal", backref="tasks")

    def to_dict(self):
        task_dict = {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "is_complete": self.completed_at is not None
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict
     
    

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            description=data["description"],
            completed_at=None
        )