import datetime
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Optional, Type, Union

import pandas as pd

from derobertis_cv.models.experience_scale import (
    HoursExperienceScale,
    SkillExperienceScale,
)
from derobertis_cv.models.i_skill_experience import ISkillExperience
from derobertis_cv.models.skill_experience_mixin import SkillExperienceMixin

if TYPE_CHECKING:
    from derobertis_cv.models.skill_experiences import SkillExperiences


@dataclass(unsafe_hash=True)
class SkillExperience(SkillExperienceMixin, ISkillExperience):
    begin_date_inp: Union[str, datetime.date]
    hours_per_week: float = 0
    one_time_hours: float = 0
    end_date_inp: Optional[Union[str, datetime.date]] = None
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale

    def __post_init__(self):
        self.begin_date = _date_str_to_date(self.begin_date_inp)
        if self.end_date_inp is not None:
            self.end_date = _date_str_to_date(self.end_date_inp)
            self.effective_end_date = self.end_date
        else:
            self.end_date = None
            self.effective_end_date = datetime.date.today()

    @property
    def hours(self) -> float:  # type: ignore
        num_hours = self.one_time_hours
        num_hours += self.weeks_elapsed * self.hours_per_week
        return num_hours

    def chain(self, other: "SkillExperience") -> "SkillExperiences":
        from derobertis_cv.models.skill_experiences import SkillExperiences

        # Create a new version of self with the end date set to the other's begin date
        self_with_end_date = replace(self, end_date_inp=other.begin_date_inp)

        return SkillExperiences(
            experiences=[self_with_end_date, other],
            experience_scale=self.experience_scale,
        )


def _date_str_to_date(date_str: str) -> datetime.date:
    dt: datetime.datetime = pd.to_datetime(date_str).to_pydatetime()
    return dt.date()
