# 불 자료형 : True or False(항상 첫 문자를 대문자로 작성해야 함)

# 불 자료형은 어떻게 사용할까?
a = True
b = False
print(type(a)) # <class 'bool'>, type(x) 는 x의 자료ㅕ형을 확인하는 파이썬 내장 함수
print(type(b)) # <class 'bool'>, type(x) 는 x의 자료ㅕ형을 확인하는 파이썬 내장 함수

# 자료형의 참과 거짓
## 문자열, 리스트, 튜플, 딕셔너리 등 값이 비어있으면 거짓, 비어있지 않으면 참이된다.
## 숫자는 0일때 거짓이된다.
## "python", [1, 2, 3], (1, 2, 3), {'a':1}, 1 => 참
## "", [], (), {}, 0, None => 거짓

# 불 연산
print(bool('python')) # True
print(bool('')) # False
print(bool([1, 2, 3])) # True
print(bool([])) # False
print(bool(0)) # False
print(bool(3)) # True