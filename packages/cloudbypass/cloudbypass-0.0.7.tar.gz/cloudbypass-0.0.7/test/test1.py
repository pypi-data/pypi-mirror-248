from src.cloudbypass import Session
from bs4 import BeautifulSoup

APIKEY = "35dc8b866b6a423caaa5f892b7d71f8b"
PROXY = "http://howard:pppppppp@47.242.250.113:10087"  # 时效代理IP
USERNAME = "18071131140telephone@gmail.com"
PASSWORD = r"B2*UK%VJg3n6_wS"

# session = Session(apikey="f84d7bc42aae407081e8a9c22c56ec2d", api_host="http://api.example.io")
session = Session(apikey=APIKEY, proxy=PROXY)

if __name__ == '__main__':
    # 先请求一次首页 获取到XSRF-TOKEN
    home_page_resp = session.request("GET", "https://visas-fr.tlscontact.com/visa/gb/gbMNC2fr/home")

    print(f"Home page resp: {home_page_resp.status_code}")
    assert home_page_resp.status_code == 200

    for cookie in home_page_resp.cookies:
        print(cookie)

    # 获取登录页面
    login_page_resp = session.request("GET", "https://visas-fr.tlscontact.com/oauth2/authorization/oidc")

    print(f"Login page resp: {login_page_resp.status_code}")
    assert login_page_resp.status_code == 200

    # 解析登录页面 form#kc-form-login
    login_page_soup = BeautifulSoup(login_page_resp.text, "html.parser")
    login_form = login_page_soup.select_one("form#kc-form-login")
    login_url = login_form.attrs.get("action")

    print(login_url)

    # 发起登录请求
    login_resp = session.request("POST", login_url, headers={
        "Content-Type": "application/x-www-form-urlencoded",
    }, data={
        "username": USERNAME,
        "password": PASSWORD,
    })

    print(f"Login resp: {login_resp.status_code}")
    assert login_resp.status_code == 200

    account_resp = session.request("GET", "https://visas-fr.tlscontact.com/api/account", )

    print(f"Account resp: {account_resp.status_code}")
    assert account_resp.status_code == 200

    print(account_resp.json())
