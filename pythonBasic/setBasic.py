# 집합 자료형은 어떻게 만들까?

## 괄호 안에 리스트 입력
s1 = set([1, 2, 3])
print(s1) # {1, 2, 3}

## 문자열 입력으로도 가능
s2 = set("Hello")
print(s2)

## 비어있는 집합 자료형
s3 = set()
print(s3)

# 집합 자료형의 특징
## 중복을 허용하지 않는다 + 순서가 없다.
## 리스트나 튜플은 순서가 있기 때문에 인덱싱을 통해 요솟값을 얻을 수 있지만 set은 순서가 없다.
## 순서가 없기 때문에 인덱싱을 통해 요솟값을 얻을 수 없다. 딕셔너리 역시 순서가 없는 자료형으로 인덱싱 제공x

## set 자료형에 저장된 값을 인덱싱으로 접근하려면 리스트나 튜플로 변환 후에 접근 해야 한다.
s1 = set([1, 2, 3])

l1 = list(s1)
print(l1) # [1, 2, 3]
print(l1[0]) # 1

t1 = tuple(s1)
print(t1) # (1, 2, 3)
print(t1[0]) # 1

# 교집합, 합집합, 차집합 구하기
s1 = set([1, 2, 3, 4, 5, 6])
s2 = set([4, 5, 6, 7, 8, 9])

## 교집합 구하기 - & or intersection
print(s1 & s2) # {4, 5, 6}
print(s1.intersection(s2)) # {4, 5, 6}

## 합집합 구하기 - | or union
print(s1 | s2)  # {1, 2, 3, 4, 5, 6, 7, 8, 9}
print(s1.union(s2)) # {1, 2, 3, 4, 5, 6, 7, 8, 9}

## 차집합 구하기 - "-" or difference
print(s1.difference(s2)) # {1, 2, 3}
print(s2.difference(s1)) # {8, 9, 7}
print(s1 - s2) # {1, 2, 3}
print(s2 - s1) # {8, 9, 7}

# 집합 자료형 관련 함수

## 값 1개 추가하기 - add
s1 = set([1, 2, 3])
s1.add(4)
print(s1) # {1, 2, 3, 4}

## 값 여러개 추가하기 - update
s1 = set([1, 2, 3])
s1.update([4, 5, 6])
print(s1) # {1, 2, 3, 4, 5, 6}

## 특정 값 제거하기 - remove
s1 = set([1, 2, 3])
s1.remove(2)
print(s1)  # {1, 3}
