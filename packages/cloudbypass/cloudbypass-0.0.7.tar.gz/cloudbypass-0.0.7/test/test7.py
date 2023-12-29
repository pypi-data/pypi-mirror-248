from src.cloudbypass import Session, Proxy

if __name__ == '__main__':
    proxy = Proxy("username-res:password")

    print("Extract dynamic proxy: ")
    print(str(proxy))
    print(str(proxy.set_region('us')))
    print("Extract Proxy with a 30-minute time limit: ")
    print(str(proxy.copy().set_expire(60 * 30).set_region('us')))

    print("Extract five 10-minute aging proxies: ")
    for _ in proxy.copy().set_expire(60 * 10).limit(5):
        print(_)

    # 循环提取
    print("Loop two 10-minute aging proxies: ")
    loop = proxy.copy().set_expire(60 * 10).set_region('US').loop(2)
    for _ in range(10):
        print(loop.__next__())