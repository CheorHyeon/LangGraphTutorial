# 딕셔너리란?
## 말 그대로 사전 이라는 뜻으로 Key와 Value를 한 쌍으로 가지는 자료형을 말한다.
## 리스트나 튜플처럼 순차적으로 해당 요솟값을 구하지 않고 Key를 통해 Value를 얻는다.

# 딕셔너리는 어떻게 만들까?
dic = {'name' : 'pey', 'phone' : '010-9999-1234', 'birth' : '1118'}
a1 = {1 : 'hi'} # key를 정수값, value로 문자열 hi를 사용한 예
a2 = {'a' : [1, 2, 3]} # Value에 리스트를 넣을 수도 있음.

# 딕셔너리 쌍 추가하기
a = {1 : 'a'}
a[2] = 'b' # key가 2이고 value가 'b'인 딕셔너리 쌍이 추가된다.
print(a) # {1: 'a', 2: 'b'}
a['name'] = 'pey'
a[3] = [1, 2, 3]
print(a) # name과 3 이란 key를 가진 쌍이 추가됨

# 딕셔너리 요소 삭제하기
del a[1] # del a[key] 사용하면 지정한 key에 해당하는 {Key:Value} 쌍이 삭제된다.
print(a) # {2: 'b', 'name': 'pey', 3: [1, 2, 3]}

# 딕셔너리 사용하는 방법

## 딕셔너리에서 Key를 사용해서 Value 얻기
## - 리스트와 튜플 문자열은 인덱싱이나 슬라이싱 기법 사용
## - 튜플은 Key를 사용해서 Value를 얻는 방법 뿐임

grade = {'pey' : 10, 'julliet' : 99}
print(grade['pey']) # 10
print(grade['julliet']) # 99

## 리스트나 튜플의 a[1]과는 전혀 다르다.
a = {1:'a', 2 : 'b'}
print(a[1]) # 'a'
print(a[2]) # 'b'

a = {'a':1, 'b':2}
print(a['a']) # 1
print(a['b']) # 2

## 위 예시 활용
dic_1 = {'name' : 'pey', 'phone' : '010-9999-1234', 'birth' : '1118'}
print(dic['phone'])
print(dic['name'])
print(dic['birth'])

# 딕셔너리 만들 때 주의사항

## Key는 고유한 값이므로 중복되는 Key 설정 시 하나를 제외한 나머지 것들이 모두 무시된다는 점에서 주의
a = {1:'a', 1 : 'b'}
print(a) # {1 : 'b'}

## Key에는 리스트를 쓸 수 없다. 하지만 튜플은 Key로 쓸 수 있다. (변할 수 없는 것만 Key로 가능)
# a = {[1, 2] : 'hi'} # 리스트를 키로 사용할 수 없다는 오류 발생

# 딕셔너리 관련 함수

## Key 리스트 만들기 - keys
### python 3.x 버전부터 변경, 리스트로 만들라면 메모리 낭비가 심해 개선됨
a = {'name' : 'pey', 'phone' : '010-9999-1234', 'birth' : '1118'}
print(a.keys()) # 딕셔너리의 key만을 모아 dict_keys 객체를 리턴, 리스트로 변환하지 않더라도 기본 반복구문 사용 가능

### dict_keys 객체는 다음과 같이 사용할 수 있다. 리스트 고유의 append, insert, pop, remove, sort 함수는 수행 불가
for k in a.keys():
    print(k)

### dict_keys 객체를 리스트로 변환
print(list(a.keys()))

## Value 리스트 만들기 - values
print(a.values()) # dict_values 객체 리턴

## Key, Value 쌍 얻기 - items
print(a.items()) # dict_items 객체 리턴

## Key:Value 쌍 모두 지우기 - clear
a.clear() # 딕셔너리 안 모든 요소 삭제
print(a)  # 빈 딕셔너리 {}로 표현

## Key로 Value 얻기 - get
a = {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118'}
print(a.get('name')) # 'pey' , a['name'] 과 동일한 결과 리턴
print(a.get('phone')) # 010-9999-1234

### a['name'] vs a.get('name')
#### 딕셔너리에 존재하지 않는 값을 가져올 떄 차이
print(a.get('nokey')) # None
# print(a['nokey']) # 에러 발생

print(a.get('nokey', 'foo')) # 없을때 None말고 기본값 지정 가능

## 해당 Key가 딕셔너리 안에 있는지 조사하기 - in
print('name' in a) # True
print('email' in a)  # False

# 내포 (dict comprehension) 형식 : 리스트를 앞에서부터 한 개씩 뽑아 변수에 담고 그 안쪽 표현식을 평가

keys = ["key1", "key2", "key3"]

dict_sam = {
    key : {
        "a1" : "a1"
    }
    for key in keys
}
print(dict_sam) # { "key1" : {"a1" : "a1"}, "key2" : { "a1", "a1" }, "key3" : { "a1", "a1" } }


dict_sam2 = {}

for key in keys:
    dict_sam2[key] = {"a1" : "a1"}

print(dict_sam2)  # { "key1" : {"a1" : "a1"}, "key2" : { "a1", "a1" }, "key3" : { "a1", "a1" } }

