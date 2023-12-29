from src.cloudbypass import Session, CloudbypassProxy

if __name__ == '__main__':
    with Session(
            apikey="35dc8b866b6a423caaa5f892b7d71f8b",
            proxy=CloudbypassProxy('22792395-res:sizrkqkb').set_region('br')#.set_expire(60 * 30)
    ) as session:
        resp = session.get("https://ipinfo.io/json")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
