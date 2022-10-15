import enum


class PLATFORM_ENUM(enum.Enum):
    DOCKER = "docker"
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    TEST = "test"

    @staticmethod
    def has_value(item):
        return item in [v.value for v in PLATFORM_ENUM.__members__.values()]

def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)

# 클래스와 데코레이터를 활용한 상수 정의
class _Constants(object):
    @constant
    def REDIS_INCREMENTS():
        return "increments"

    @constant
    def REDIS_QUEUE():
        return "redis_queue"


CONSTANTS = _Constants()
