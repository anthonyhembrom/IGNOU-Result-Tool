import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "gradecard_results.txt"

TARGET_COURSES = [
    "BCS051",
    "BCS052",
    "BCS053",
    "BCS054",
    "BCS055",
    "BCSL056",
    "BCSL057",
    "BCSL058"
]

def safe_int(value):
    try:
        return int(value)
    except:
        return 0

def print_and_save(results):

    os.system("cls" if os.name == "nt" else "clear")

    results_sorted = sorted(
        results,
        key=lambda x: x["TOTAL"],
        reverse=True
    )

    header = (
        f"{'ENROLLMENT':<12} | "
        f"{'NAME':<25} | "
        f"{'051':<4} | "
        f"{'052':<4} | "
        f"{'053':<4} | "
        f"{'054':<4} | "
        f"{'055':<4} | "
        f"{'056':<4} | "
        f"{'057':<4} | "
        f"{'058':<4} | "
        f"{'TOTAL':<5}"
    )

    print(header)
    print("-" * len(header))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        f.write(header + "\n")
        f.write("-" * len(header) + "\n")

        for r in results_sorted:

            line = (
                f"{r['enrollment']:<12} | "
                f"{r['name'][:25]:<25} | "
                f"{r['BCS051']:<4} | "
                f"{r['BCS052']:<4} | "
                f"{r['BCS053']:<4} | "
                f"{r['BCS054']:<4} | "
                f"{r['BCS055']:<4} | "
                f"{r['BCSL056']:<4} | "
                f"{r['BCSL057']:<4} | "
                f"{r['BCSL058']:<4} | "
                f"{r['TOTAL']:<5}"
            )

            print(line)
            f.write(line + "\n")


with open("student_list.txt", "r", encoding="utf-8") as f:
    enrollments = [x.strip() for x in f if x.strip()]

results = []

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

for enr in enrollments:

    try:

        url = (
            f"https://gradecard.ignou.ac.in/"
            f"view_gradecard.aspx?"
            f"eno={enr}&prog=BCAOL&type=1"
        )

        response = session.get(url, timeout=10)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        name_tag = soup.find(
            id="ctl00_ContentPlaceHolder1_lblDispname"
        )

        name = (
            name_tag.get_text(strip=True)
            if name_tag
            else "NOT FOUND"
        )

        marks = {
            "BCS051": "ND",
            "BCS052": "ND",
            "BCS053": "ND",
            "BCS054": "ND",
            "BCS055": "ND",
            "BCSL056": "ND",
            "BCSL057": "ND",
            "BCSL058": "ND"
        }

        table = soup.find(
            id="ctl00_ContentPlaceHolder1_gvDetail"
        )

        if table:

            rows = table.find_all("tr")

            for row in rows:

                cols = row.find_all("td")

                if len(cols) < 2:
                    continue

                course = cols[0].get_text(strip=True)

                if course in TARGET_COURSES:

                    assignment = cols[1].get_text(strip=True)

                    marks[course] = assignment

        total = (
            safe_int(marks["BCS051"]) +
            safe_int(marks["BCS052"]) +
            safe_int(marks["BCS053"]) +
            safe_int(marks["BCS054"]) +
            safe_int(marks["BCS055"]) +
            safe_int(marks["BCSL056"]) +
            safe_int(marks["BCSL057"]) +
            safe_int(marks["BCSL058"])
        )

        results.append({
            "enrollment": enr,
            "name": name,
            "BCS051": marks["BCS051"],
            "BCS052": marks["BCS052"],
            "BCS053": marks["BCS053"],
            "BCS054": marks["BCS054"],
            "BCS055": marks["BCS055"],
            "BCSL056": marks["BCSL056"],
            "BCSL057": marks["BCSL057"],
            "BCSL058": marks["BCSL058"],
            "TOTAL": total
        })

        print_and_save(results)

    except Exception:

        results.append({
            "enrollment": enr,
            "name": "ERROR",
            "BCS051": "ERR",
            "BCS052": "ERR",
            "BCS053": "ERR",
            "BCS054": "ERR",
            "BCS055": "ERR",
            "BCSL056": "ERR",
            "BCSL057": "ERR",
            "BCSL058": "ERR",
            "TOTAL": 0
        })

        print_and_save(results)

print("\nFinished. Results saved to:", OUTPUT_FILE)