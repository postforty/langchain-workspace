from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., description="사용자의 이름")
    age: int = Field(..., gt=0, description="사용자의 나이 (0보다 커야 함)") # greater than
    email: str | None = None # 선택적 필드

user1 = User(name="김일남", age=99, email="kim1@example.com")
print(user1)

user2 = User(name="김이남", age=98)
print(user2)

user3 = User(name="김삼남", age="구십칠")
print(user3)

