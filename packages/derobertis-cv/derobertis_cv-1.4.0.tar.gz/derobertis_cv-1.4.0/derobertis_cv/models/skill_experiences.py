import datetime
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Sequence, Type

from derobertis_cv.models.experience_scale import (
    HoursExperienceScale,
    SkillExperienceScale,
)
from derobertis_cv.models.i_skill_experience import ISkillExperience
from derobertis_cv.models.skill_experience import SkillExperience
from derobertis_cv.models.skill_experience_mixin import SkillExperienceMixin

if TYPE_CHECKING:
    from derobertis_cv.models.skill_experience import SkillExperience


@dataclass(unsafe_hash=True)
class SkillExperiences(SkillExperienceMixin, ISkillExperience):
    experiences: Sequence[SkillExperience]
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale

    def __post_init__(self):
        count_end_date = sum(
            1 if exp.end_date is not None else 0 for exp in self.experiences
        )
        if count_end_date < len(self.experiences) - 1:
            raise SkillExperienceInputValidationException(
                experiences=self.experiences,
                message="Can only have one experience with no end date (only one can go to present)",
            )

    @property
    def begin_date(self) -> datetime.date:  # type: ignore
        return min(exp.begin_date for exp in self.experiences)

    @property
    def effective_end_date(self) -> datetime.date:  # type: ignore
        return max(exp.effective_end_date for exp in self.experiences)

    @property
    def hours(self) -> float:  # type: ignore
        return sum(exp.hours for exp in self.experiences)

    def chain(self, other: "SkillExperiences | SkillExperience") -> "SkillExperiences":
        other_experiences = (
            other.experiences if isinstance(other, SkillExperiences) else [other]
        )

        # Need to set the end date of the last current experience to the begin of the first incoming experience
        new_last_prior_experience = replace(
            self.experiences[-1], end_date_inp=other_experiences[0].begin_date_inp
        )
        prior_experiences = [*self.experiences[:-1], new_last_prior_experience]

        return SkillExperiences(
            experiences=[*prior_experiences, *other_experiences],
            experience_scale=self.experience_scale,
        )


@dataclass(frozen=True)
class SkillExperienceInputValidationException(Exception):
    experiences: Sequence[SkillExperience]
    message: str

    def __str__(self):
        return f"{self.message}:\n{self.experiences}"
