import pyexlatex.resume as lr

from derobertis_cv import plbuild
from derobertis_cv.pldata.constants.contact import CONTACT_LINES
from derobertis_cv.pldata.cv import (
    CVModel,
    ResumeSection,
    get_cv_contents,
    get_cv_packages,
    get_cv_pre_env_contents,
)

AUTHORS = ["Nick DeRobertis"]

DOCUMENT_CLASS = lr.Resume
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None


SECTIONS = [ResumeSection.REFERENCES]


def get_content():
    model = CVModel(
        SECTIONS,
    )
    contents = get_cv_contents(model, include_self_image=False)
    return contents


DOCUMENT_CLASS_KWARGS = dict(
    contact_lines=CONTACT_LINES,
    packages=get_cv_packages(),
    pre_env_contents=get_cv_pre_env_contents(),
)
OUTPUT_NAME = f"{AUTHORS[0]} References"
