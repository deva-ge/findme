import requests, os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def normalize_query(query):
    # Заменяем пробелы на подчеркивание
    normalized_query = query.replace(" ", "_")

    # Удаляем другие недопустимые символы в именах директорий
    normalized_query = ''.join(char for char in normalized_query if char.isalnum() or char in ['_', '-'])

    return normalized_query

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

def create_html_file(repositories, search_query, days_threshold,main_directory="."):

    normalized_search_query = normalize_query(search_query)

    html_directory = os.path.join(main_directory, normalized_search_query)
    
    
     # ᲕᲐᲛᲝᲬᲛᲔᲑᲗ ᲐᲠᲘᲡ ᲗᲣ ᲐᲠᲐ ᲓᲘᲠᲔᲥᲢᲝᲠᲘᲐ
    if not os.path.exists(html_directory):
        # თუ არ არსებობს, ვქმნით დირექტორიას
        os.makedirs(html_directory)
        print(f"ᲓᲘᲠᲔᲥᲢᲝᲠᲘᲐ '{normalized_search_query}' ᲐᲠ ᲘᲧᲝ ᲓᲐ ᲨᲔᲕᲥᲛᲔᲜᲘ.")
    
    html_path = os.path.join(html_directory, "active_repo.html")
    with open(html_path, "w") as file:
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
        file.close()
        
def read_token_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"ფაილი '{filename}' ვერ მოიძებნა.")
        return None

if __name__ == "__main__":
    search_query = input("ᲨᲔᲘᲧᲕᲐᲜᲔᲗ ᲫᲔᲑᲜᲘᲡ ᲨᲔᲙᲕᲔᲗᲐ (ᲛᲐᲒᲐᲚᲘᲗᲐᲓ, 'open source'): ")
    days_threshold = int(input("ᲨᲔᲘᲧᲕᲐᲜᲔᲗ ᲓᲦᲔᲔᲑᲘᲡ ᲠᲐᲝᲓᲔᲜᲝᲑᲐ ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲘᲡ ᲐᲥᲢᲘᲕᲝᲑᲘᲡ ᲒᲐᲜᲡᲐᲖᲐᲖᲦᲕᲠᲐᲓ: "))

    main_directory = "repos"
    
    threshold_date = datetime.now() - timedelta(days=days_threshold)
    
    access_token = read_token_from_file('token.txt')  # ᲩᲔᲛᲘ ᲢᲝᲙᲔᲜᲘ
    repositories = search_github_repositories(search_query, access_token)
    
  

    if repositories:
        active_repositories = [repo for repo in repositories if is_recently_active(repo, threshold_date)]
        if active_repositories:
            create_html_file(active_repositories, search_query, days_threshold,search_query,main_directory)
            print(f"ᲨᲔᲓᲔᲒᲘ ᲬᲐᲠᲛᲐᲢᲔᲑᲘᲗ ᲩᲐᲘᲬᲔᲠᲐ ᲤᲐᲘᲚᲨᲘ active-repo.html.")
        else:
            print("ᲐᲡᲔᲗᲘ ᲐᲥᲢᲘᲕᲝᲑᲘᲡ ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲔᲑᲘ ᲐᲠ ᲛᲝᲘᲫᲔᲑᲜᲐ.")
    else:
        print("ᲠᲔᲞᲝᲖᲘᲢᲝᲠᲘᲔᲑᲘ ᲐᲠ ᲛᲝᲘᲫᲔᲑᲜᲐ.")
