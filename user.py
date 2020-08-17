from dataclasses import dataclass
from eip712_structs import EIP712Struct, Uint, String

class UserSol(EIP712Struct):
  name = String()
  age = Uint()

  def say_values(self) -> (String, Uint):
      return self.name, self.age

@dataclass
class User:
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def values(self) -> (str, int):
        return self.name, self.age