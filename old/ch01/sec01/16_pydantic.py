# 데이터 유효성 검사
from pydantic import BaseModel, Field

# gt(greater than): 지정 숫자보다 커야함
class User(BaseModel):
    name: str = Field(description="사용자의 이름")
    age: int = Field(gt=0, description="사용자의 나이(0보다 커야 함)")
    # email: str | None = None
    email: str = Field(default="이메일 없음")

try:
    user1 = User(name="김일남", age=99, email="kim1@example.com")
    print(user1)

    user2 = User(name="김이남", age=98)
    print(user2)
except Exception as e:
    print(f"유효성 검사 오류: {e}")