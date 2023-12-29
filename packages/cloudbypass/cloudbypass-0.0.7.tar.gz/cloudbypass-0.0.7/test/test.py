from src.cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="35dc8b866b6a423caaa5f892b7d71f8b") as session:
        resp = session.get("https://opensea.io/category/memberships")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
