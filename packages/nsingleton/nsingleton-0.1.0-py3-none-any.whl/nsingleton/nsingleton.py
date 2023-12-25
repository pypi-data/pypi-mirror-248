import threading
from typing import Any, Type, TypeVar, cast

T = TypeVar("T")  # Generic type variable


class _SingletonWrapper:
    """A singleton wrapper class. Instances are created for each decorated class."""

    def __init__(self, cls: Type[T]):
        self.__wrapped__ = cls
        self._instance = None
        self._instance_created = False
        self.lock = threading.Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Returns a single instance of the decorated class."""
        if not self._instance_created:
            with self.lock:
                if not self._instance_created:
                    try:
                        self._instance = self.__wrapped__(*args, **kwargs)
                    except Exception as e:
                        raise RuntimeError(
                            f"Error creating instance of {self.__wrapped__.__name__}"
                        ) from e
                    self._instance_created = True
        return self._instance


def singleton(cls: Type[T]) -> Type[T]:
    """
    A singleton decorator. Returns a wrapper object. A call on that object
    returns a single instance object of the decorated class. Use the __wrapped__
    attribute to access the decorated class directly in unit tests.
    """
    wrapper = _SingletonWrapper(cls)
    return cast(Type[T], wrapper)
