from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., description="사용자 이름")
    age: int = Field(..., gt=0, description="사용자의 나이 (0보다 커야 함)")
    email: str | None = None

try:
    user1 = User(name="김일남", age=99, email="kim1@example.com")
    print(user1)
    print(user1.model_dump_json(indent=2))

    user2 = User(name="김이남", age=-98)
except Exception as e:
    print(e)