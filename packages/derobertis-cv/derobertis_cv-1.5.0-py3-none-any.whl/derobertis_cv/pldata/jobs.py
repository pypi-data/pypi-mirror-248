import datetime
from typing import Callable, Dict, List, Optional, Sequence

from derobertis_cv import logger
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pldata.courses.main import get_courses
from derobertis_cv.pldata.employment_model import (
    AcademicEmploymentModel,
    EmploymentModel,
    JobIDs,
    filter_jobs,
)
from derobertis_cv.pldata.universities import UF, VCU


def get_professional_jobs(
    excluded_companies: Optional[Sequence[str]] = None,
    include_private: bool = False,
    modify_descriptions: Optional[
        Dict[JobIDs, Callable[[Sequence[str]], Sequence[str]]]
    ] = None,
) -> List[EmploymentModel]:
    jobs = [
        EmploymentModel(
            JobIDs.EVB_PORTFOLIO_ANALYST.value,
            [
                r"Rebuilt Allowance for Loan and Lease Losses (ALLL) models, ultimately saving $5.4 million "
                r"for the bank",
                "Developed probability of default (PD) and loss given default (LGD) statistics for over "
                "10,000 commercial and consumer loans by internal risk grade, delinquency status, "
                "and FFIEC code using migration analysis",
                "Designed and implemented stress testing methodologies",
            ],
            "Eastern Virginia Bankshares",
            "Portfolio Analyst, Portfolio Management",
            "Atlee, VA",
            datetime.datetime(2012, 8, 15),
            datetime.datetime(2013, 8, 15),
            company_short_name="EVB",
            short_job_title="Analyst",
            hours_per_week=30,
        ),
        EmploymentModel(
            JobIDs.CNC_MP.value,
            [
                "Analyzed financial information obtained from clients to determine strategies for meeting "
                "their financial objectives",
                "Gathered data on market conditions to inform clients of threats and opportunities",
                "Recommended to clients financial strategies in cash management, investment planning, or other areas "
                "to help them achieve their financial goals",
            ],
            "CNC Partners",
            "Managing Partner",
            "Richmond, VA",
            datetime.datetime(2013, 5, 15),
            datetime.datetime(2014, 8, 15),
            company_short_name="CNC",
            short_job_title="MP",
            hours_per_week=5,
        ),
        EmploymentModel(
            JobIDs.FRB_INTERN.value,
            [
                "Created a regulatory scale which standardizes the largest banks' internal ratings",
                "Analyzed the Shared National Credit (SNC) program to reduce inefficiencies "
                "and implemented a data pipeline to improve usability of data",
            ],
            "Federal Reserve Board of Governors",
            "Credit Risk Intern, Banking Supervision & Regulation",
            "Washington, D.C.",
            datetime.datetime(2011, 5, 15),
            datetime.datetime(2011, 8, 15),
            company_short_name="FRBG",
            short_job_title="Intern",
            hours_per_week=40,
        ),
        EmploymentModel(
            JobIDs.PARLIAMENT_TUTOR.value,
            [
                "Assisted students with homework, projects, test preparation, papers, research in master's and "
                "undergraduate finance courses",
                "Taught skills to improve academic performance, including study strategies, "
                "note-taking skills and approaches to answering test questions",
            ],
            "Parliament Tutors",
            "Tutor",
            "Gainesville, FL",
            datetime.datetime(2017, 9, 1),
            end_date=datetime.datetime(2021, 4, 12),
            company_short_name="PT",
            short_job_title="Tutor",
            hours_per_week=3,
        ),
        EmploymentModel(
            JobIDs.CLAIMFOUND_CTO.value,
            [
                "Created the business that ultimately grew to 15 employees, raised $1.75M, "
                "and was acquired by Carbon Health Technologies, with only one co-founder",
                "Managed up to 10 software developers, providing technical guidance and tracking progress, using "
                "a custom management system designed based on agile practices",
                "Architected a web application with a Python Flask back-end API and a TypeScript Angular front-end "
                "to assist individuals in claiming lost money",
                "Designed and implemented data pipelines that clean and aggregate state unclaimed property data "
                "into a 3NF schema in a PosgreSQL database hosted in AWS RDS",
                "Developed the full-stack prototype of the application and deployed it using Docker Swarm on "
                "AWS EC2 instances",
                "Secured, monitored, and managed the application by developing encryption, rate limiting, active monitoring "
                "services, user analytics, and operator interfaces",
                "Optimized consumer funnel by analyzing conversions in an A/B testing framework",
                "Automated testing, data pipelines, and deployment using Python and Bash scripts, "
                "AWS CLI, and Gitlab CI/CD",
                "Strategized about product development to improve user experience (UX) and monetization while appeasing "
                "regulatory concerns",
                "Assessed and refined product-market fit by developing detailed financial models and updating them "
                "with information learned from user analytics, user feedback, and regulatory response",
            ],
            "Claimfound, Inc.",
            "Co-Founder and Chief Technology Officer",
            "Gainesville, FL",
            datetime.datetime(2016, 8, 15),
            end_date=datetime.datetime(2022, 12, 31),
            company_short_name="CF",
            short_job_title="CTO",
            hours_per_week=40,
        ),
        EmploymentModel(
            JobIDs.CARBON_HEALTH_SENIOR.value,
            [
                "Collaborated with product, design, data science, and other engineers to release features that "
                "improve the productivity of clinicians and support staff",
                "Architected and executed large projects to improve the Scala monolith, "
                "Kotlin microservices, and React Native mobile and web applications",
                "Optimized performance of existing product features by implementing caching, "
                "query optimization, reducing component renders, and re-architecting with GraphQL "
                "to minimize data transfer",
                "Refined organizational engineering practices by contributing to discussions and documentation",
                "Assisted in training and hiring of new engineers",
            ],
            "Carbon Health Technologies",
            "Senior Software Engineer",
            "San Francisco, CA",
            datetime.datetime(2021, 4, 12),
            end_date=datetime.datetime(2022, 8, 31),
            company_short_name="CH",
            short_job_title="Senior Eng",
            hours_per_week=40,
        ),
        EmploymentModel(
            JobIDs.CARBON_HEALTH_STAFF.value,
            [
                "Collaborate with product, design, data science, and other engineers to release features that "
                "improve the productivity of clinicians and support staff",
                "Architect, execute, and direct others through large projects to improve the Scala monolith, "
                "Kotlin microservices, and React Native mobile and web applications",
                "Introduce technical approaches and patterns, anticipating and responding to the organization's needs",
                "Optimize performance of existing product features by implementing caching, "
                "query optimization, reducing component renders, and re-architecting with GraphQL "
                "and NextJS to minimize client data transfer",
                "Establish new applications and application monitoring infrastructure",
                "Refine organizational engineering practices by contributing to discussions and documentation",
                "Assist in training and hiring of new engineers",
            ],
            "Carbon Health Technologies",
            "Staff Software Engineer",
            "San Francisco, CA",
            datetime.datetime(2022, 9, 1),
            company_short_name="CH",
            short_job_title="Staff Eng",
            hours_per_week=40,
        ),
        EmploymentModel(
            JobIDs.COVARIANCE_PM_ENG.value,
            [
                "Analyze complex problems and create workflows involving humans and automation",
                "Design and implement software to automate workflows and improve efficiency",
                "Contribute to overall product strategy and technical platform",
            ],
            "Stealth Mode Startup",
            "Lead Product Manager and Engineer",
            "New York, NY",
            datetime.datetime(2022, 11, 25),
            company_short_name="Stealth",
            short_job_title="PM & Eng",
            hours_per_week=20,
        ),
        EmploymentModel(
            JobIDs.SPENDOSO_CTO.value,
            [
                "Architect a web application with a Python FastAPI back-end and a TypeScript NextJS front-end "
                "to assist companies with managing their software spending",
                "Manage 2 software developers, providing technical guidance and tracking progress, using "
                "a custom management system designed based on agile practices",
                "Design and implement data pipelines that regularly sync SSO and financial data "
                "into a 3NF schema in a PosgreSQL database hosted in AWS RDS",
                "Develop the full-stack application and deployed it using Terraform on "
                "AWS Fargate and Vercel",
                "Secure, monitor, and manage the application by developing encryption, rate limiting, active monitoring "
                "services, user analytics, and operator interfaces",
                "Automate testing, data pipelines, and deployment using Python, Airflow, Terraform, and Github Actions",
                "Strategize about product development to improve user experience (UX) and monetization",
                "Assess and refine product-market fit by developing detailed financial models and updating them "
                "with information learned from user analytics and user feedback",
            ],
            "Spendoso, LLC",
            "Co-Founder and Chief Technology Officer",
            "Sheridan, WY",
            datetime.datetime(2022, 8, 1),
            company_short_name="Spendoso",
            short_job_title="CTO",
            hours_per_week=10,
        ),
    ]
    if include_private:
        try:
            from private_cv.jobs import get_professional_jobs as get_private_jobs
        except ModuleNotFoundError:
            logger.warn(
                "Could not find private_cv module, skipping private jobs even though they were requested"
            )
        else:
            jobs.extend(get_private_jobs())
    jobs = filter_jobs(
        jobs,
        excluded_companies=excluded_companies,
        modify_descriptions=modify_descriptions,
    )
    return jobs


def get_academic_jobs(
    excluded_companies: Optional[Sequence[str]] = None,
    modify_descriptions: Optional[
        Dict[JobIDs, Callable[[Sequence[str]], Sequence[str]]]
    ] = None,
) -> List[AcademicEmploymentModel]:
    courses = get_courses()
    uf_courses = [
        course
        for course in courses
        if course.university and course.university.title == UF_NAME
    ]
    vcu_courses = [
        course
        for course in courses
        if course.university and course.university.title == VCU_NAME
    ]

    jobs = [
        AcademicEmploymentModel(
            JobIDs.UF_GA.value,
            [
                "Conduct full research projects, including project development, data collection, and "
                "analysis",
                "Analyze billions of data points of panel- and time-series data using econometric models "
                "and techniques such as OLS, Logit, Probit, Fama-MacBeth, "
                "ARIMA, vector autoregression, Granger causality, hazard, quantile, "
                "PCA, LDA, EFA, CFA, SEM, difference-in-differences, and propensity score matching",
                "Predict and classify outcomes using machine learning models such as "
                "deep learning (multilayer perceptron), SVM, "
                "K-nearest neighbors, K-means, decision trees, "
                "ridge, LASSO, naive Bayes, and ensemble methods",
                "Collect data using web-scraping, APIs, and databases",
                "Clean, aggregate, and merge data from multiple sources with outliers and errors "
                "at different frequencies and levels of aggregation",
            ],
            UF.title,
            "Graduate Assistant",
            "Gainesville, FL",
            begin_date=datetime.datetime(2014, 8, 15),
            end_date=datetime.datetime(2021, 5, 31),
            courses_taught=uf_courses,
            company_short_name=UF.abbreviation,
            short_job_title="GA",
            hours_per_week=30,
        ),
        AcademicEmploymentModel(
            JobIDs.VCU_GA.value,
            [
                "Perform multivariate linear and non-linear analyses on collected data to answer research questions",
                "Assist professors in teaching responsibilities, such as teaching class sections and grading "
                "student assignments and examinations",
                "Present research findings in an effective manner",
            ],
            VCU.title,
            "Graduate Assistant",
            "Richmond, VA",
            begin_date=datetime.datetime(2013, 9, 1),
            end_date=datetime.datetime(2014, 8, 15),
            courses_taught=vcu_courses,
            company_short_name=VCU.abbreviation,
            short_job_title="GA",
            hours_per_week=30,
        ),
    ]

    jobs = filter_jobs(jobs, excluded_companies=excluded_companies, modify_descriptions=modify_descriptions)  # type: ignore
    return jobs


def _return_first(description: Sequence[str]) -> Sequence[str]:
    return description[0]


def _return_two(description: Sequence[str]) -> Sequence[str]:
    return description[:2]


def _return_first_and_third(description: Sequence[str]) -> Sequence[str]:
    return [description[0], description[2]]


def _replace_vcu_ga_description(description: Sequence[str]) -> Sequence[str]:
    return [
        "Conduct research and assist professors in teaching class sections and grading assignments",
    ]


CV_JOB_MODIFIERS: Dict[JobIDs, Callable[[Sequence[str]], Sequence[str]]] = {
    JobIDs.CNC_MP: _return_first,
    JobIDs.VCU_GA: _replace_vcu_ga_description,
}

CV_EXCLUDED_COMPANIES: List[JobIDs] = [
    JobIDs.PARLIAMENT_TUTOR,
    JobIDs.CNC_MP,
]
