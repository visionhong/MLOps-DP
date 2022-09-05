import enum


class PLATFORM_ENUM(enum.Enum):
    DOCKER = "docker"
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    TEST = "test"

    @staticmethod  # 정적 메서드를 활용해 클래스선언 없이 바로 함수로 접근 가능
    def has_value(item):  # item으로 들어오는 문자열이 전역변수의 값들을 담은 list에 있는지 True or False
        return item in [v.value for v in PLATFORM_ENUM.__members__.values()]


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _Constants(object):
    @constant  # 위에 constant 함수의 인자 f가 아래 함수가 됨
    def REDIS_INCREMENTS():
        return "increments"

    @constant
    def REDIS_QUEUE():
        return "redis_queue"


CONSTANTS = _Constants()
