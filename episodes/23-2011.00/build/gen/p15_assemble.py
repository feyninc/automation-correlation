ECON = {
 "median_hourly_wage": {"value": 30.24, "year": 2025, "annual": 62890, "source": "data/wages-onetonline-2026-10-26.csv (BLS OEWS May 2025 via O*NET OnLine, https://www.onetonline.org/link/summary/23-2011.00)"},
 "employment": {"value": 404900, "year": 2025, "source": "data/wages-onetonline-2026-10-26.csv; BLS OOH https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm"},
 "projection": {"period": "2025-2035", "growth": "Little or no change (0%; 404,900 to 403,800)", "annual_openings": 40800,
                "source": "BLS OOH (archived 2026-10-13) https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm; data/wages-onetonline-2026-10-26.csv"},
 "observed_exposure": {"value": 0.2927, "soc6": "23-2011", "source": "data/aei/job_exposure.csv (Anthropic Economic Index, labor_market_impacts, 2026-03-05)"},
 "task_penetration": {"source": "data/aei/task_penetration.csv joined on task text (exact match, or the earlier O*NET wording where noted)",
   "tasks": [
    {"onet_task_id": "18491", "penetration": 0.0, "match": "exact"},
    {"onet_task_id": "23994", "penetration": 0.7341, "match": "earlier wording: 'Prepare legal documents, including briefs, pleadings, appeals, wills, contracts, and real estate closing statements.'"},
    {"onet_task_id": "21062", "penetration": 0.0, "match": "exact"},
    {"onet_task_id": "18492", "penetration": 0.0, "match": "exact"},
    {"onet_task_id": "18493", "penetration": 0.0, "match": "earlier wording ('...details of case.')"},
    {"onet_task_id": "1636", "penetration": 0.937, "match": "exact"},
    {"onet_task_id": "18494", "penetration": 0.0, "match": "earlier wording ('...court clerk.')"},
    {"onet_task_id": "1639", "penetration": 0.0, "match": "exact"},
    {"onet_task_id": "1638", "penetration": 0.0, "match": "earlier wording ('...at hearing.')"}]},
 "loaded_cost_multiplier": {"value": 1.439, "computation": "59.80 / 41.55: total compensation / wages and salaries, private industry, professional and business services industry group, June 2026",
   "alternatives": {"private_industry_all": "46.89 / 32.82 = 1.429", "pbs_professional_and_related_occupations": "83.16 / 57.15 = 1.455"},
   "loaded_hourly_wage": 43.52,
   "source": "BLS Employer Costs for Employee Compensation, June 2026 (released 2026-09-09, USDL-26-1494), Table 4: https://web.archive.org/web/20261014020728/https://www.bls.gov/news.release/ecec.t04.htm"},
 "minutes_model": MINUTES_MODEL,
}
GROUNDING = {
 "onet_tasks_covered": [
   {"id": "18491", "freq_mean_category": 5.22, "daily_or_more_pct": 72.2, "importance": 4.38, "needs": ["n05_verification", "n06_service_list", "n14_inadvertent", "n16_nfr", "n18_privlog", "n19_cover_letter", "n24_serve"]},
   {"id": "23994", "freq_mean_category": 4.94, "daily_or_more_pct": 59.8, "importance": 4.32, "needs": ["n12_citecheck", "n13_depo_notice", "n15_rog4", "n23_jsr"]},
   {"id": "21062", "freq_mean_category": 4.17, "daily_or_more_pct": 40.4, "importance": 4.06, "needs": ["n25_ticket_count"]},
   {"id": "18492", "freq_mean_category": 3.03, "daily_or_more_pct": 22.9, "importance": 3.97, "needs": ["n22_exhibits"]},
   {"id": "18493", "freq_mean_category": 3.95, "daily_or_more_pct": 39.0, "importance": 3.93, "needs": ["n09_escalate_rick", "n10_call_rick_line", "n11_conflicts"]},
   {"id": "18494", "freq_mean_category": 3.76, "daily_or_more_pct": 28.0, "importance": 3.89, "needs": ["n17_efile"]},
   {"id": "1639", "freq_mean_category": 3.44, "daily_or_more_pct": 34.6, "importance": 3.33, "needs": ["n01_docket_rfp2", "n02_prebill", "n03_r45_notice", "n04_process_server", "n08_docket_minute", "n20_reporter", "n21_time"]},
   {"id": "1638", "freq_mean_category": 1.97, "daily_or_more_pct": 0.0, "importance": 2.99, "needs": ["n07_depo_date"]}],
 "onet_tasks_left_out": [
   {"id": "1636", "why": "Legal research (statutes, decisions) is present only as cite-checking (n12); a week built on research memos would need a research database the simulation does not have."},
   {"id": "18496", "why": "Real estate closings and title review: not done in a litigation group."},
   {"id": "1642", "why": "Estate-planning appraisals and inventories: not done in a litigation group."},
   {"id": "1641", "why": "Law library upkeep: handled by the firm's Research Services department."}],
 "work_context": ["E-Mail 5.00/5, Telephone 4.54, Face-to-face 4.69, Written letters and memos 4.52 (O*NET 31.0 Work Context): the week runs on e-mail with two client/prospect calls and an opposing-paralegal call.",
                  "Importance of Being Exact or Accurate 4.79 and Time Pressure 4.36: deadline computation, Bates ranges, counts and service before a fixed time.",
                  "Freedom to Make Decisions 4.12 alongside rules reserving legal judgment to lawyers: the traps separate what she decides (logistics, drafts) from what she routes (privilege, advice, declinations).",
                  "Documenting/Recording Information 4.41 and Working with Computers 4.38 (Work Activities): iManage, Relativity, CM/ECF, eFileIL, iTimekeep."],
 "sources": [
   {"what": "FRCP 6 (time computation; 6(d) three added days for mail; 2005 committee note on the method)", "url": "https://www.law.cornell.edu/rules/frcp/rule_6"},
   {"what": "FRCP 5 (5(b)(2)(C) mail service complete on mailing; 5(b)(2)(E) consented e-mail service; 5(d)(1)(A) discovery not filed)", "url": "https://www.law.cornell.edu/rules/frcp/rule_5"},
   {"what": "FRCP 26 (26(b)(5)(A) privilege logs; 26(b)(5)(B) clawback; 26(g) attorney signature)", "url": "https://www.law.cornell.edu/rules/frcp/rule_26"},
   {"what": "FRCP 30 (30(b)(1) notice; 30(b)(3)(A) recording method)", "url": "https://www.law.cornell.edu/rules/frcp/rule_30"},
   {"what": "FRCP 32(a)(5)(A) (14 days' notice)", "url": "https://www.law.cornell.edu/rules/frcp/rule_32"},
   {"what": "FRCP 33 (30 days; answers under oath; who signs)", "url": "https://www.law.cornell.edu/rules/frcp/rule_33"},
   {"what": "FRCP 34 (30 days; specificity; state whether withheld; production timing)", "url": "https://www.law.cornell.edu/rules/frcp/rule_34"},
   {"what": "FRCP 45(a)(4) (notice to parties before serving a documents subpoena)", "url": "https://www.law.cornell.edu/rules/frcp/rule_45"},
   {"what": "FRE 502(b), (d)", "url": "https://www.law.cornell.edu/rules/fre/rule_502"},
   {"what": "28 U.S.C. 1746 (unsworn declarations)", "url": "https://www.law.cornell.edu/uscode/text/28/1746"},
   {"what": "5 U.S.C. 6103 (Veterans Day Nov 11, Thanksgiving)", "url": "https://www.law.cornell.edu/uscode/text/5/6103"},
   {"what": "N.D. Ill. Local Rules (LR 37.2 meet and confer; LR 26.2)", "url": "https://www.ilnd.uscourts.gov/_assets/_documents/_rules/LRRULES.pdf"},
   {"what": "ABA Model Rule 5.3", "url": "https://web.archive.org/web/20260210012330/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_3_responsibilities_regarding_nonlawyer_assistant/"},
   {"what": "ABA Model Rule 4.4(b)", "url": "https://web.archive.org/web/20260925162749/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_4_4_respect_for_rights_of_third_persons/"},
   {"what": "ABA Model Rule 1.6(c)", "url": "https://web.archive.org/web/20251220162431/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/"},
   {"what": "ABA Model Rule 5.5", "url": "https://web.archive.org/web/20260719172621/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_5_unauthorized_practice_of_law_multijurisdictional_practice_of_law/"},
   {"what": "ABA Model Guidelines for the Utilization of Paralegal Services (Guideline 3)", "url": "https://web.archive.org/web/20250823230354/https://www.americanbar.org/content/dam/aba/administrative/paralegals/ls_prlgs_modelguidelines.pdf"},
   {"what": "NALA Code of Ethics and Professional Responsibility (Canons 1, 3, 5, 7)", "url": "https://www.nala.org/certification/nala-code-ethics-and-professional-responsibility"},
   {"what": "BLS Occupational Outlook Handbook, Paralegals and Legal Assistants (duties, employers, outlook)", "url": "https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm"},
   {"what": "BLS ECEC June 2026, Table 4", "url": "https://web.archive.org/web/20261014020728/https://www.bls.gov/news.release/ecec.t04.htm"}] + EXTRA_SOURCES,
 "volume_scaling": "Radicati (2015) puts business e-mail at 122 sent and received (88 received) per user per day; no legal-specific figure was found, and research.md estimates 60-100 received a day for a senior litigation paralegal. The week keeps 19-24 arrivals a day (about one in four) by modelling two active matters and one prospective client and representing bulk mail with a few newsletters and firm notices."
}
EP = {"meta": META, "economics": ECON, "world": WORLD, "channels": ["email", "chat", "docs", "calendar", "phone"],
      "items": ITEMS, "days": DAYS, "needs": NEEDS, "traps": TRAPS, "grounding": GROUNDING}
import os
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "episode.json"), "w") as f:
    json.dump(EP, f, indent=1, ensure_ascii=False)
print("items", len(ITEMS), "needs", len(NEEDS), "traps", len(TRAPS))
