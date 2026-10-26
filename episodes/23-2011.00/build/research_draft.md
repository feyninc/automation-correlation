# 23-2011.00 Paralegals and Legal Assistants: research for the episode

Drafted 2026-10-26 for schema v0.1. Every number below carries a URL or a local path. Where no source was found, the
number is labelled an estimate and the reasoning is given. Web pages on bls.gov and americanbar.org refuse this
computer, so they are cited through dated Wayback Machine captures of the official pages.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $30.24 (annual $62,890), May 2025 | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine); same figure in BLS OOH ([archived 2026-10-13](https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm)) |
| Wage spread | 10th percentile $44,740; 90th percentile $101,500 a year; legal services industry median $61,770 | BLS OOH (archived, as above) |
| Employment | 404,900 (2025) | `data/wages-onetonline-2026-10-26.csv`; BLS OOH |
| Projection 2025-2035 | Little or no change: 0%, 404,900 to 403,800; about 40,800 openings a year, mostly replacement | BLS OOH Job Outlook tab (archived, as above). The OOH adds that demand "is expected to be limited by advances in technology, including artificial intelligence (AI)". |
| Where they work | Legal services 75%; local government 5%; federal 4%; state 3%; finance and insurance 3% | BLS OOH Work Environment tab |
| Anthropic observed exposure | 0.2927 (SOC 23-2011) | `data/aei/job_exposure.csv` |
| Loaded-cost multiplier | 1.439 | BLS ECEC June 2026 (released 2026-09-09, USDL-26-1494), Table 4, private industry, professional and business services industry group: total compensation $59.80 / wages and salaries $41.55 an hour worked ([Table 4, archived 2026-10-14](https://web.archive.org/web/20261014020728/https://www.bls.gov/news.release/ecec.t04.htm)). Alternatives from the same table: all private industry 46.89 / 32.82 = 1.429; professional and related occupations within professional and business services 83.16 / 57.15 = 1.455. |
| Loaded hourly cost | $43.52 = $30.24 x 1.439 | computed |

Why that ECEC cell: 75% of paralegals work in legal services (NAICS 5411), which sits in the professional and
business services supersector; ECEC does not publish legal services alone. Paralegals are a professional-and-related
occupation in ECEC's grouping, which would give 1.455; the industry-group figure (1.439) is used because it covers
all occupations in the employers that hire them, and the difference is 1%.

### Per-task penetration (Anthropic Economic Index)

Joined `data/aei/task_penetration.csv` on task text. Five of the twelve O*NET 31.0 statements do not match exactly
because 31.0 reworded them; for those the earlier O*NET wording in the file was used (noted).

| Task ID | Task (O*NET 31.0) | Frequency: share daily or more | Importance (1-5) | Penetration |
| --- | --- | --- | --- | --- |
| 18491 | Prepare affidavits or other documents, such as legal correspondence, and organize and maintain documents in paper or electronic filing system | 72.2% | 4.38 | 0.0 |
| 23994 | Prepare, edit, or review legal documents, including legislation, briefs, pleadings, appeals, wills, contracts, and real estate closing statements | 59.8% | 4.32 | 0.7341 (earlier wording "Prepare legal documents, including briefs, pleadings, ...") |
| 21062 | Investigate facts and law of cases and search pertinent sources ... to determine causes of action and to prepare cases | 40.4% | 4.06 | 0.0 |
| 18492 | Prepare for trial by performing tasks such as organizing exhibits | 22.9% | 3.97 | 0.0 |
| 18493 | Meet with clients and other professionals to discuss details of cases | 39.0% | 3.93 | 0.0 (earlier wording "...details of case.") |
| 1636 | Gather and analyze research data, such as statutes, decisions, and legal articles, codes, and documents | 43.9% | 3.89 | 0.937 |
| 18494 | File pleadings with court clerks | 28.0% | 3.89 | 0.0 (earlier wording "...court clerk.") |
| 1639 | Direct and coordinate law office activity, including delivery of subpoenas | 34.6% | 3.33 | 0.0 |
| 1638 | Call upon witnesses to testify at hearings | 0.0% | 2.99 | 0.0 (earlier wording "...at hearing.") |
| 18496 | Arbitrate disputes between parties and assist in the real estate closing process | 25.8% | 2.99 | 0.0 |
| 1642 | Appraise and inventory real and personal property for estate planning | 23.6% | 2.90 | 0.0 |
| 1641 | Keep and monitor legal volumes to ensure that the law library is up-to-date | 1.9% | 2.67 | 0.0 (earlier wording) |

Frequency is from O*NET 31.0 `Task Ratings.txt` (scale FT; categories 5-7 = daily, several times daily, hourly or
more); importance is scale IM. Script: the join was run over `data/onet/db_31_0_text/Task Statements.txt`, `Task
Ratings.txt` and `data/aei/task_penetration.csv`.

Reading of the penetration numbers: Claude use concentrates on the two writing-and-research tasks (1636 at 0.94,
23994 at 0.73) and is zero on everything procedural or relational: filing, docketing, subpoena logistics, client
contact, trial prep. Most of this week's needs are in exactly that procedural zero-penetration band, which is what an
anticipating assistant would have to break into.

### Minutes model

The schema's defaults are reading at 238 words a minute (Brysbaert 2019) and a composing speed. For this occupation:

MINUTES_SECTION

## 2. The job as it is really done

JOB_SECTION

## 3. Why this week, and what it covers

WEEK_SECTION

## 4. Scaling real volumes down

SCALING_SECTION

## 5. What could not be sourced

UNSOURCED_SECTION

## 6. Sources

SOURCES_SECTION
