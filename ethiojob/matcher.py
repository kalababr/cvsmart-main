import json


with open("jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)


cv_text = "python developer django sql html css javascript"


def match_score(cv_text, job_desc):
    score = 0
    for word in cv_text.lower().split():
        if word in job_desc.lower():
            score += 1
    return score


for job in jobs:
    desc = job.get("description", "")
    job["score"] = match_score(cv_text, desc)

jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)


for job in jobs[:5]:
    print("Title:", job["title"])
    print("Score:", job["score"])
    print("Link:", job["link"])
    print("-" * 40)