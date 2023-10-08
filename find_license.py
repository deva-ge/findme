"""
სკრიპტი მოძებნის პროექტში ლიცენზიის ფაილს.
"""
import requests
from bs4 import BeautifulSoup

def check_open_source(project_url):
    response = requests.get(project_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # შემოწმება, არის თუ არა ფალი LICENSE რეპოზიტორიაში
        license_file = soup.find('a', {'title': 'LICENSE'})
        if license_file:
            print("პროექტი შეიცავს ფაილს LICENSE, რაც უჩვენებს ლიცენზიის არსებობას.")
        else:
            print("პროექტი არ შეიცავს ფაილს LICENSE, რაც შეიძლება ნიშნავდეს იმას, რომ არ აქვს გაცხადებული ლიცენზია.")

        # README.md ფაილში ლიცენზიის განყოფილების შემოწმება
        readme_section = soup.find('div', {'id': 'readme'})
        if readme_section:
        
            license_text = readme_section.find('a', {'title': 'License'})
            if license_text:
                print("ლიცენზია მითითებულია განყოფილებაში README.")
    else:
        #  ToDO: გავაკეთო ცნობილი შეცდომების გადარჩევა და შესაბამისი შეტყობინებების დაბჭვდა
        
        # თუ რეპოზიტორის გვერდზე შეცდომაა, მაშინ დაბეჭდება შეტყობინება
        print("ვერ მოხერხდა დაშვება რეპოზიტორის გვერდზე. სტატუს კოდი:", response.status_code)

if __name__ == "__main__":
    project_url = "https://github.com/deva-ge/findme"  # Замените на URL репозитория
    check_open_source(project_url)
