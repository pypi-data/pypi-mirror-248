from nsingleton import singleton


def test_singleton_decorator():
    @singleton
    class TestClass:
        def __init__(self):
            self.value = 1

    instance1 = TestClass()
    instance2 = TestClass()

    assert instance1 is instance2, "Singleton instances are not the same"


def test_singleton_decorator_with_different_classes():
    @singleton
    class TestClass1:
        def __init__(self):
            self.value = 1

    @singleton
    class TestClass2:
        def __init__(self):
            self.value = 2

    instance1 = TestClass1()
    instance2 = TestClass2()

    assert (
        instance1 is not instance2
    ), "Singleton instances from different classes are the same"


def test_singleton_decorator_with_wrapped_attribute():
    @singleton
    class TestClass:
        def __init__(self):
            self.value = 1

    assert hasattr(
        TestClass, "__wrapped__"
    ), "Singleton does not have __wrapped__ attribute"


def test_singleton_decorator_with_wrapped_class():
    @singleton
    class TestClass:
        def __init__(self):
            self.value = 1

    WrappedClass = TestClass.__wrapped__
    instance1 = WrappedClass()
    instance2 = WrappedClass()

    assert instance1 is not instance2, "Instances from the wrapped class are the same"
