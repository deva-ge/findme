import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def search_github_repositories(query, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc"
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        repositories = data.get('items', [])
        return repositories
    else:
        print("ᲛᲝᲜᲐᲪᲔᲛᲔᲑᲘᲡ ᲛᲘᲦᲔᲑᲐ ᲐᲠ ᲒᲐᲛᲝᲕᲘᲓᲐ. ᲨᲔᲪᲓᲝᲛᲘᲡ ᲙᲝᲓᲘ:", response.status_code)
        return []

def is_recently_active(repo, threshold_date):
    last_activity = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
    return last_activity >= threshold_date

def create_html_file(repositories, search_query, days_threshold):
    with open("dist/active-repo.html", "w") as file:
        file.write("<html><body>\n")
        file.write(f"<h1>ᲦᲘᲐ ᲡᲐᲛᲔᲪᲜᲘᲔᲠᲝ ᲠᲔᲞᲝᲖᲘᲖᲝᲠᲘᲔᲑᲘ</h1>\n")
        file.write(f"<h2>ᲫᲔᲑᲜᲘᲡ ᲞᲐᲠᲐᲛᲔᲢᲠᲔᲑᲘ: </h2>\n")
        file.write(f"<p>ᲨᲔᲙᲕᲔᲗᲐ: {search_query.upper()}, </p>\n")
        file.write(f"<p>ᲐᲥᲢᲘᲕᲝᲑᲘᲡ ᲕᲐᲓᲐ (ᲓᲦᲔᲔᲑᲨᲘ): {days_threshold}</p>\n")
        file.write(f"<ul>\n")
        for repo in repositories:
            file.write(f'<li>\n')
            file.write(f'  <a href="{repo["html_url"]}">{repo["full_name"]}</a>\n')
            file.write(f'  <p>ᲑᲝᲚᲝ ᲐᲥᲢᲘᲕᲝᲑᲐ: {repo["pushed_at"]}</p>\n')
            file.write(f'</li>\n')
        file.write("</ul>\n")
        file.write("</body></html>")

if __name__ == "__main__":
    search_query = input("ᲨᲔᲘᲧᲕᲐᲜᲔᲗ ᲫᲔᲑᲜᲘᲡ ᲨᲔᲙᲕᲔᲗᲐ (ᲛᲐᲒᲐᲚᲘᲗᲐᲓ, 'open source'): ")
    days_threshold = int(input("ᲨᲔᲘᲧᲕᲐᲜᲔᲗ ᲓᲦᲔᲔᲑᲘᲡ ᲠᲐᲝᲓᲔᲜᲝᲑᲐ ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲘᲡ ᲐᲥᲢᲘᲕᲝᲑᲘᲡ ᲒᲐᲜᲡᲐᲖᲐᲖᲦᲕᲠᲐᲓ: "))
    
    threshold_date = datetime.now() - timedelta(days=days_threshold)
    
    access_token = "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"  # ᲩᲔᲛᲘ ᲢᲝᲙᲔᲜᲘ
    repositories = search_github_repositories(search_query, access_token)

    if repositories:
        active_repositories = [repo for repo in repositories if is_recently_active(repo, threshold_date)]
        if active_repositories:
            create_html_file(active_repositories, search_query, days_threshold)
            print(f"ᲨᲔᲓᲔᲒᲘ ᲬᲐᲠᲛᲐᲢᲔᲑᲘᲗ ᲩᲐᲘᲬᲔᲠᲐ ᲤᲐᲘᲚᲨᲘ active-repo.html.")
        else:
            print("ᲐᲡᲔᲗᲘ ᲐᲥᲢᲘᲕᲝᲑᲘᲡ ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲔᲑᲘ ᲐᲠ ᲛᲝᲘᲫᲔᲑᲜᲐ.")
    else:
        print("ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲔᲑᲘ ᲐᲠ ᲛᲝᲘᲫᲔᲑᲜᲐ.")
