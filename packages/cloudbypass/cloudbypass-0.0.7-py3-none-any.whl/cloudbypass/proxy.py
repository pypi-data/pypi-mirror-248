import random
import re


class CloudbypassProxy:
    # 默认网关
    __default_gateway = 'gw.cloudbypass.com:1288'

    def __init__(self, auth, **kwargs):
        """
        :param auth: format: 12345678-res:password
        """
        self.__username, self.__password = self.check_auth(auth)
        self.__region = kwargs.get('region')
        self.__expire = kwargs.get('expire', 0)
        self.__session_id = None

    def set_expire(self, expire):
        """
        :param expire: Unit: second
        :return:
        """
        self.__expire = expire
        self.__session_id = None
        return self

    def set_dynamic(self):
        """
        :return:
        """
        return self.set_expire(0)

    def set_gateway(self, gateway):
        """
        :param gateway:
        :return:
        """
        self.__default_gateway = gateway
        self.__session_id = None
        return self

    def set_region(self, region):
        """
        :param region:
        :return:
        """
        self.__region = region
        self.__session_id = None
        return self

    def clear_region(self):
        """
        :return:
        """
        self.__region = None
        self.__session_id = None
        return self

    @property
    def username(self):
        """
        :return:
        """
        return self.__username

    @property
    def password(self):
        """
        :return:
        """
        return self.__password

    @property
    def gateway(self):
        """
        :return:
        """
        return self.__default_gateway

    @property
    def expire(self):
        """
        :return:
        """
        return self.__expire

    @staticmethod
    def check_auth(auth):
        """
        :param auth:
        :return:
        """
        if auth is None or re.match(r'^\w+-(res|dat):\w+$', auth) is None:
            raise ValueError('Invalid auth format')

        return auth.split(':')

    @property
    def session_id(self):
        """
        :return:
        """
        # __session_id
        if self.__session_id is None:
            self.__session_id = "".join(
                random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=11)
            )

        return self.__session_id

    def __parse_options(self):
        options = [
            self.username,
        ]
        expire = self.expire if isinstance(self.expire, int) and 0 < self.expire <= 5184000 else None

        if self.__region is not None:
            options.append(self.__region.replace(' ', '+'))

        if expire is not None:
            for time, unit in [(60, 's'), (60, 'm'), (24, 'h'), (999, 'd')]:
                if expire < time or expire % time:
                    options.append(f'{self.session_id}-{expire}{unit}')
                    break
                expire //= time

        return '_'.join(options)

    def format(self, format_str='{username}:{password}@{gateway}'):
        """
        :param format_str: {username}:{password}@{gateway}
        :return:
        """
        return format_str.format(
            username=self.__parse_options(),
            password=self.password,
            gateway=self.gateway
        )

    def limit(self, count):
        """
        :param count:
        :return:
        """
        if count <= 0:
            raise ValueError('count must be greater than 0')

        for _ in range(count):
            yield self.__next__()

    def loop(self, count):
        """
        :param count:
        :return:
        """
        __pool = []

        if count <= 0:
            raise ValueError('count must be greater than 0')

        for _ in self.limit(count):
            __pool.append(_)
            yield _

        while True:
            for _ in __pool:
                yield _

    def copy(self):
        """
        Copy a new proxy
        :return:
        """
        return self.__copy__()

    def __str__(self):
        """
        :return:
        """
        return self.format()

    def __repr__(self):
        """
        :return:
        """
        return self.__str__()

    def __copy__(self):
        """
        Copy a new proxy
        :return:
        """
        return CloudbypassProxy(f"{self.username}:{self.password}", **{
            'region': self.__region,
            'expire': self.__expire,
        })

    def __iter__(self):
        """
        :return:
        """
        return self

    def __next__(self):
        """
        :return:
        """
        self.__session_id = None
        return self.__copy__()
