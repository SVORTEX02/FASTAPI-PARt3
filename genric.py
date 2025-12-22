from typing import Generic, TypeVar

T = TypeVar("Pandya")


class Holder(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get_value(self) -> T:
        return self.value

h2 = Holder[str]("fastapi")
h3 = Holder[float](3.14)


print(h2.get_value())
print(h3.get_value())
