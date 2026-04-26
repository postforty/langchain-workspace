from pydantic import BaseModel, Field

# 데이터 스키마(schema) 정의
# 유효성 검사
class User(BaseModel):
    name: str = Field(description="사용자의 이름")
    age: int = Field(gt=0, description="사용자의 나이")
    email: str | None = None

user1 = User(name="김일남", age=99, email="kim1@example.com")
print(user1)

user2 = User(name="김이남", age=98)
print(user2)