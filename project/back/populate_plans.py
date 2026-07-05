import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from product.models import Plan, Recommend, Operation, Production, Item

# 데이터 초기화 (기존 데이터 삭제)
Plan.objects.all().delete()
Recommend.objects.all().delete()
Operation.objects.all().delete()
Production.objects.all().delete()
Item.objects.all().delete()

# Recommend 데이터 생성
r1, _ = Recommend.objects.get_or_create(name="영상 마케팅 입문 기업")
r2, _ = Recommend.objects.get_or_create(name="내부 인력이 없는 기업")
r3, _ = Recommend.objects.get_or_create(name="채널 성장과 브랜딩까지")
r4, _ = Recommend.objects.get_or_create(name="원하는 기업")

# Operation 데이터 생성
o1, _ = Operation.objects.get_or_create(name="꾸준한 업로드와")
o2, _ = Operation.objects.get_or_create(name="채널 운영")
o3, _ = Operation.objects.get_or_create(name="채널 성장, 구매 전환 설계")
o4, _ = Operation.objects.get_or_create(name="전문성 브랜딩")

# Production 데이터 생성
p1, _ = Production.objects.get_or_create(name="월 1회 방문 촬영")
p2, _ = Production.objects.get_or_create(name="4편 제작")
p3, _ = Production.objects.get_or_create(name="월 1회 방문 촬영+협의")
p4, _ = Production.objects.get_or_create(name="4편 + 별도 쇼츠 4회")

# Item 데이터 생성
i_basic = [
    "기본 편집", "자막 편집", "썸네일 제작", "업로드 관리", "채널 운영 관리", "[병원일 경우] 의료광고 표현 리스크 기본 검토"
]
i_growth = i_basic + [
    "프리미엄(디자인) 편집", "썸네일 고도화 기획", "기본 성과 분석", "성과 분석 리포트", "채널 전략 설계", "쇼츠/숏폼 재가공", "SNS 관리 + [인스타, 틱톡]"
]

items_basic = [Item.objects.get_or_create(name=name)[0] for name in i_basic]
items_growth = [Item.objects.get_or_create(name=name)[0] for name in i_growth]

# BASIC Plan 생성
plan_basic = Plan.objects.create(
    plan_type="BASIC",
    name="Basic Channel Operation",
    subname="베이직 채널 운영",
    price=250
)
plan_basic.recommends.add(r1, r2)
plan_basic.operations.add(o1, o2)
plan_basic.productions.add(p1, p2)
for i in items_basic:
    plan_basic.items.add(i)

# GROWTH Plan 생성
plan_growth = Plan.objects.create(
    plan_type="GROWTH",
    name="YouTube Growth Package",
    subname="유튜브 성장 패키지",
    price=350
)
plan_growth.recommends.add(r3, r4)
plan_growth.operations.add(o3, o4)
plan_growth.productions.add(p3, p4)
for i in items_growth:
    plan_growth.items.add(i)

print("성공적으로 요금제 초기 데이터를 삽입했습니다.")
