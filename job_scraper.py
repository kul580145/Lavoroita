import requests

ADZUNA_APP_ID = "ce090eea"
ADZUNA_APP_KEY = "c4ff95d10c0314f758bab13a2e086917"

def scrape_jobs(position: str):
    all_jobs = []
    
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/it/search/1"
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": position,
            "where": "Italia",
            "results_per_page": 20
        }
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        
        for job in data.get("results", []):
            all_jobs.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "site": "Adzuna.it",
                "url": job.get("redirect_url", "")
            })
    except Exception as e:
        print(f"Adzuna error: {e}")
    
    print(f"মোট {len(all_jobs)} টি জব পাওয়া গেছে")
    return all_jobs
