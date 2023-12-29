from cloudbypass import Session

if __name__ == '__main__':
    session = Session(apikey="35dc8b866b6a423caaa5f892b7d71f8b")
    resp = session.get("https://etherscan.io/accounts/label/lido")
    print(resp.status_code, resp.headers.get("x-cb-status"))
    print(resp.text)