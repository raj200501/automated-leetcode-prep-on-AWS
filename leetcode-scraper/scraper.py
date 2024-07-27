import requests
import json

def scrape_leetcode_problems():
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)
    problems = response.json()
    with open('problems.json', 'w') as f:
        json.dump(problems, f)

if __name__ == "__main__":
    scrape_leetcode_problems()
