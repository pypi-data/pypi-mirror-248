from src.cloudbypass import Session, Proxy

if __name__ == '__main__':
    proxy = Proxy('username-res:password')
    print(proxy.set_expire(60 * 30).set_region('us'))
    print(proxy)
    print(proxy.copy().set_expire(60 * 10).set_region('us'))
    print(proxy.copy().set_expire(60 * 10 + 1).set_region('us'))
    print(proxy.copy().set_dynamic().set_region('us'))
    print(proxy.__copy__().set_expire(60 * 10).set_region('us'))
    print(proxy.__copy__().clear_region().set_expire(0))
    print(proxy)
