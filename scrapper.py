import requests
from bs4 import BeautifulSoup

URL = "https://www.linkedin.com/jobs/search?keywords=Desenvolvedor&location=Sorocaba%2C%20S%C3%A3o%20Paulo%2C%20Brasil&geoId=100218040&distance=25&f_TPR=r604800&position=1&pageNum=0"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def find_linkedin_jobs():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    job_listings = soup.find_all('div', class_='base-card')

    for job in job_listings:
        title_tag = job.find('h3', class_='base-search-card__title')
        company_tag = job.find('h4', class_='base-search-card__subtitle')
        link_tag = job.find('a', class_='base-card__full-link')
        location_tag = job.find('span', class_='job-search-card__location')

        if title_tag and company_tag and link_tag:
            job_data = {
                'title': title_tag.get_text(strip=True),
                'company': company_tag.get_text(strip=True),
                'link': link_tag['href'].split('?')[0]
            }
            if location_tag:
                job_data['location'] = location_tag.get_text(strip=True)
            jobs.append(job_data)
    return jobs

