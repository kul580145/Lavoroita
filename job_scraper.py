import requests
from bs4 import BeautifulSoup

def scrape_jobs(position: str):
    all_jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    # Indeed Italy
    try:
        url = f"https://it.indeed.com/jobs?q={position}&l=Italia"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for card in soup.find_all("div", class_="job_seen_beacon")[:5]:
            title = card.find("h2")
            company = card.find("span", class_="companyName")
            link = card.find("a")
            all_jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "site": "Indeed.it",
                "url": "https://it.indeed.com" + link["href"] if link else ""
            })
    except Exception as e:
        print(f"Indeed error: {e}")

    # InfoJobs Italy
    try:
        url = f"https://www.infojobs.it/offerte-lavoro/{position}"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for card in soup.find_all("li", class_="ij-OfferCard")[:5]:
            title = card.find("h2")
            company = card.find("span", class_="ij-OfferCard-description-header-company")
            all_jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "site": "InfoJobs.it",
                "url": ""
            })
    except Exception as e:
        print(f"InfoJobs error: {e}")

    # Monster Italy
    try:
        url = f"https://www.monster.it/lavoro/cerca?q={position}"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for card in soup.find_all("div", class_="job-cardstyle__JobCardComponent")[:5]:
            title = card.find("h3")
            company = card.find("span", class_="job-cardstyle__CompanyName")
            all_jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "site": "Monster.it",
                "url": ""
            })
    except Exception as e:
        print(f"Monster error: {e}")

    print(f"মোট {len(all_jobs)} টি জব পাওয়া গেছে")
    return all_jobs
