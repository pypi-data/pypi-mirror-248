from dataclasses import dataclass

from typing_extensions import Self

from derobertis_cv.models.skill import SkillModel
from derobertis_cv.pldata.skills import get_skills


@dataclass
class SkillHours:
    name: str
    hours: float | None

    @classmethod
    def from_skill_model(cls, model: SkillModel) -> Self:
        return cls(
            name=model.to_title_case_str(),
            hours=int(model.experience.hours) if model.experience else None,
        )


def get_skill_hours() -> list[SkillHours]:
    return [SkillHours.from_skill_model(model) for model in get_skills()]


if __name__ == "__main__":
    from pprint import pprint

    models = sorted(get_skill_hours(), key=lambda model: model.hours or 0, reverse=True)
    pprint(models)
