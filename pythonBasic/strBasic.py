# 문자열 자료형

# 문자열을 어떻게 만들고 사용할까?

## 큰 따옴표로 양쪽 둘러싸기
print(type("Hello World")) # <class 'str'>

## 작은따옴표로 양쪽 둘러싸기
print(type('Python is fun'))

## 큰따옴표 3개를 연속으로 써서 양쪽 둘러싸기
print(type("""Life is too short, You need python"""))

## 작은따옴표 3개를 연속으로 써서 양쪽 둘러싸기
print(type('''Life is too short, You need python'''))

# 문자열 안에 작음 따옴표나 큰 따옴표롤 포함시키고 싶을 때

## 1. 문자열에 작은 따옴표 포함하기
food = "Python's favorite food is perl"
print(food)

### 작은따옴표로 둘러싸고 실행 - 구문 오류 발생 ('Python'이 문자로 인식됨)
# food = 'Python's favorite food is perl'
# print(food)

## 2. 문자열에 큰따옴표 포함하기
say = '"Python is very easy." he says.'
print(say)

## 3. 역슬래시를 사용해서 작은따옴표와 큰 따옴표 문자열에 포함하기
food = 'Python\'s favorite food is perl'
print(food)
say = "\"Python is very easy.\" he says."
print(say)

# 여러 줄인 문자열을 변수에 대입하고 싶을 때

## 1. 줄을 바꾸기 위한 이스케이프 코드 `\n` 삽입하기
multiline = "Life is too short\nYou need python"
print(multiline)

## 2. 연속된 작은따옴표 3개 또는 큰따옴표 3개 사용하기
multiline = '''
    Life is too short
    You need python
    '''
print(multiline)

multiline = """
    Life is too short
    You need python
    """
print(multiline)

## 이스케이프 문자 사용해도 되지만 멀티라인이 더 깔끔

# 문자열 연산하기

## 문자열 더해서 연결하기
head = "Python"
tail = " is fun!"
print(head + tail) # Python is fun!

## 문자열 곱하기
a = "python"
print(a * 2) # pythonpython

## 문자열 길이 구하기
a = "Life is too short"
print(len(a)) # 17

# 문자열 인덱싱(가리킨다) 과 슬라이싱(잘라 낸다)

## 문자열 인덱싱
a = "Life is too short, You need python"
print(a[3]) # 'e'

## 문자열 슬라이싱
b = a[0] + a[1] + a[2] + a[3]
print(b) # 'Life'
print(a[0:4]) # 'Life'
print(a[5:7]) # 'is' , 시작번호 0일 필요 없다
print(a[19:]) # 'You need Python', 끝 번호 부분 생략하면 시작 번호부터 그 문자열의 끝까지 뽑아낸다
print(a[:17]) # 'Life is too short', 시작 번호 생략 시 문자열의 처음부터 끝 번호까지 뽑아 낸다.
print(a[:]) # "Life is too short, You need python", 시작 번호와 끝 번호를 생략하면 문자열의 처음부터 끝까지 뽑아 낸다.
print(a[19:-7]) # 'You need', a[-7] 미포함

# 문자열 변경
a = "Pithon"
print(a[1]) # 'i'
# a[1] = 'y'  # 오류 발생, 문자열의 요소는 변경 불가, 슬라이싱 기법 사용해야 함

print(a[:1]) # 'P'
print(a[2:]) # 'thon'
print(a[:1] + 'y' + a[2:]) # 'Python'

# 문자열 포매팅 - 문자열 안의 특정 값을 바꿔야 할 경우

## 1. 숫자 바로 대입
print("I eat %d apples." % 3)

## 2. 문자열 바로 대입
print("I eat %s apples. " % "five")

## 3. 숫자 값을 나타내는 변수 대입
number = 3
print("I eat %d apples." % number)

## 2개 이상의 값 넣기
number = 10
day = "three"
print("I ate %d apples. so I was sick for %s days." % (number, day))

# 문자열 포맷 코드
## %s : 문자열 / %c 문자 1개 / %d 정수 / %f 부동소수 / %o 8진수 / %x 16진수 / %% Literal 문자(%자체)

## %s의 경우 어떤 형태는 값을 변환해 넣을 수 있다.
print("I have %s apples." % 3) # I have 3 apples
print("rate is %s" % 3.234) # rate is 3.234

## '%d' + "%' 형태를 쓰려면 '%%' 형태로 써야한다.
# print("Error is %d%" % 98) # 오류 발생
print("Error is %d%%" % 98)

# 포맷 코드와 숫자 함께 사용하기

## 1. 정렬과 공백
print("%10s" % "hi") # 10s는 전체 길이가 10개인 문자열 공간에서 대입되는 값 오른쪽 정렬하고 나머지 공백
print("%-10sjane." % 'hi') #'hi        jane' 왼쪽정렬 -10

## 2. 소수점 표현하기
print("%0.4f" % 3.42136234) # '3.4214', 0을 생략해도됨, 소수점 4번째 자리까지만(5번쨰 자리 반올림)
print("%10.4f" % 3.42134234) #    3.4213, 앞에 공백4자리 포함하여 오른쪽 정렬

# format 함수를 사용한 포매팅

## 숫자 바로 대입하기
print("I eat {0} apples".format(3)) # I eat 3 apples
print("I eat {0} apples".format("five")) # I eat five apples

## 숫자 값을 가진 변수로 대입하기
number = 3
print("I eat {0} apples".format(number)) # I eat 3 apples

## 2개 이상의 값 넣기
number = 10
day = "three"
print("I ate {0} apples. so I was sick for {1} days.".format(number, day))

## 이름으로 넣기
print("I ate {number} apples. so I was sick for {day} days.".format(number=number, day=day))

## 인덱스와 이름을 혼용해서 넣기
print("I ate {0} apples. so I was sick for {day} days.".format(10, day=day))

## 왼쪽 정렬
print("{0:<10}".format("hi")) # hi        , :<10 표현식을 사용하면 치환되는 문자열 왼쪽 정렬 + 총 자리수 10

## 오른쪽 정렬
print("{0:>10}".format("hi")) #         hi, :>10 표현식을 사용하면 치환되는 문자열 왼쪽 정렬 + 총 자리수 10

## 가운데 정렬
print("{0:^10}".format("hi"))   #    hi    , :^를 사용하면 가운데 정렬도 가능하다.

## 공백 채우기 : 정렬 문자 `<`, `>`, `^` 바로 앞에 넣어서 정렬 시 공백 문자 대신 지정한 문자로 채울 수 있다.
print("{0:=^10}".format("hi")) # ====hi====
print("{0:!<10}".format("hi")) # hi!!!!!!!!

## 소수점 표현하기
y = 3.41234234
print("{0:0.4f}".format(y)) # 3.4123
print("{0:10.4f}".format(y)) # '    3.4213'

# { 또는 } 문자 표현하기
print("{{ and }}".format())  # format 함수를 사용해 포매팅 시 중괄호 문자를 문자 그대로 사용하고 싶은 경우 2개 연속 사용

# f 문자열 포매팅 - 문자열 앞에 f 붙이면 f 문자열 포매팅
name = '홍길동'
age = 30
print(f'나의 이름은 {name}입니다. 나이는 {age} 입니다.') # 나의 이름은 홍길동입니다. 나이는 30 입니다.

## f문자열 포매팅은 표현식(중괄호 안의 변수를 계산식과 함께 사용하는 것)을 제공한다.
age = 30
print(f'나는 내년이면 {age + 1}살이 된다.')

## 딕셔너리는 f문자열 포매팅에서 다음과 같이 사용할 수 있다.
d = {'name' : '홍길동', 'age' : 30}
print(f'나의 이름은 {d["name"]}입니다. 나이는 {d["age"]}입니다.')

## 정렬
print(f'{"hi":<10}') # 왼쪽정렬
print(f'{"hi":>10}') # 오른쪽정렬
print(f'{"hi":^10}') # 가운데 정렬

## 공백 채우기
print(f'{"hi":=^10}') #가운데 정렬 =로 공백채우기
print(f'{"hi":!<10}') #왼쪽 정렬하고 '!' 문자로 공백 채우기

## 소수점
y = 3.41234234
print(f'{y:0.4f}') #3.4123, 소수점 4자리 까지만
print(f'{y:10.4f}') #     3.4123, 총 자리수 10, 소수점 4자리

## {}를 문자 그대로 표시하려면 2개 동시 사용
print(f'{{ and }}') # { and }

## f문자열을 사용하여 금액에 콤마 삽입하기
print(f'난 {15000000:,}원이 필요해')

# 문자열 관련 함수

## 문자 개수 새기
a = "hobby"
print(a.count('b')) # 2

## 위치 알려 주기 1 - find
a = "Python is the best choice"
print(a.find('b')) # 14
print(a.find('k')) # -1 (찾는 문자나 문자열이 존재하지 않는 경우)

## 위치 알려 주기 2 - index
a = "Life is too short"
print(a.index('t')) # 8
# print(a.index('k'))  # 찾는 문자나 문자열 존재하지 않으면 오류 발생

## 문자열 삽입 - join
print(",".join('abcd')) # 문자 사이 ',' 삽입
print(",".join(['a', 'b', 'c', 'd'])) # a,b,c,d

## 소문자를 대문자로 바꾸기 - upper (이미 대문자라면 아무 변화 없음)
a = "hi"
print(a.upper())

ab = "영어와 hi가 섞이면?"
print(ab.upper())  # 영어와 HI가 섞이면?

## 대문자를 소문자로 바꾸기 - lower
a = "HI"
print(a.lower()) # hi

ab = "영어와 HI가 섞이면?"
print(ab.lower()) # 영어와 hi가 섞이면?

## 왼쪽 공백 지우기 - lstrip
a = " hi "
print(a.lstrip()) # "hi "

## 오른쪽 공백 지우기 - rstrip
a = " hi "
print(a.rstrip()) # " hi"

## 양쪽 공백 지우기 - strip
a = " hi "
print(a.strip()) # "hi"

## 문자열 바꾸기 - replace
a = "Life is too short"
print(a.replace("Life", "Your leg")) # 문자열 안의 특정 값을 다른 값으로 치환해 준다.

## 문자열 나누기 - split 결과는 리스트
a = "Life is too short"
print(a.split()) # ['Life', 'is', 'too', 'short'], 아무것도 없으면 공백(스페이스, 탭, 엔터) 기준 문자열

b = "a:b:c:d"
print(b.split(":")) # 특정 값이 있을 때면 괄호 안을 구분자로 나눠줌

## 문자열이 알파벳으로만 구성되어 있는지 확인하기 - isalpha
s = "Python"
print(s.isalpha()) # True

s = "Python3"
print(s.isalpha()) # False

s = "Hello World"
print(s.isalpha()) # False, 공백 문자가 포함되었기 때문

## 문자열이 숫자로만 구성되어 있는지 확인하기 - isdigit
s = "12345"
print(s.isdigit()) # True

s = "1234a"
print(s.isdigit()) # False

s = " 12 34"
print(s.isdigit())  # False , 공백 포함

## 문자열이 특정 문자(열)로 시작하는지 확인하기 - startswith
s = "Life is too short"
print(s.startswith("Life"))  # True
print(s.startswith("short")) # False

## 문자열이 특정 문자(열)로 끝나는지 확인하기 - endswith
s = "Life is too short"
s.endswith("short") # True
s.endswith("too") # False

## 착각하기 쉬운 문자열 함수

### upper를 수행하더라도 a의 값은 변하지 않는다. 문자열은 변경 불가능한 자료형
a = 'hi'
a.upper() # 'HI'
print(a) # 'hi'

### 바꾸고 싶다면 대입문 사용해야 한다.
a = a.upper()
print(a)

## 나머지 함수들도 모두 동일, 불변 자료형