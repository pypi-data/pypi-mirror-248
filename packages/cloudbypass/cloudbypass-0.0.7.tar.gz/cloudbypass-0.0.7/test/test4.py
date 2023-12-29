from src.cloudbypass import Session
from bs4 import BeautifulSoup

APIKEY = "35dc8b866b6a423caaa5f892b7d71f8b"
PROXY = "http://howard:pppppppp@47.242.250.113:10087"  # 时效代理IP


if __name__ == '__main__':
    with Session(apikey=APIKEY, proxy=PROXY) as session:
        resp = session.get("https://etherscan.io/accounts/label/lido", part="0")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
