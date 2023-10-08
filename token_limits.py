import requests
from read_token import read_token_from_file


access_token = read_token_from_file('token.txt')  # GitHub ტოკენი ფაილიდან
url = "https://api.github.com/rate_limit"

headers = {
    "Authorization": f"token {access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("API შეკვეთების ლიმიტი GitHub-ზე:")
    print("ლიმიტი:", data["resources"]["core"]["limit"])
    print("გამოყენებულია:", data["resources"]["core"]["used"])
    print("დარჩა:", data["resources"]["core"]["remaining"])
else:
    print("ვერ მოხერხდა ლიმიტების შესახებ ინფორმაციის მიღება. შეცდომის კოდი:", response.status_code)
