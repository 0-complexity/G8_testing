from requests import HTTPError
from test_suite.orchestrator_objects.orchestrator_driver import OrchasteratorDriver


def catch_exception_decoration(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HTTPError as e:
            if e.status_code == 440:
                self.orchasterator_driver = OrchasteratorDriver()
                wrapper(self, *args, **kwargs)
            else:
                return e.response

    return wrapper
