import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from work.models import MainCategory, SubCategory, Work

print("Cleaning existing dummy works...")
Work.objects.all().delete()
SubCategory.objects.all().delete()
MainCategory.objects.all().delete()

print("Creating categories...")
main_com, _ = MainCategory.objects.get_or_create(name='COMMERCIAL', order=1)
main_mv, _ = MainCategory.objects.get_or_create(name='MUSIC VIDEO', order=2)
main_shorts, _ = MainCategory.objects.get_or_create(name='SHORTS', order=3)

sub_nike, _ = SubCategory.objects.get_or_create(main_category=main_com, name='나이키 글로벌', order=1)
sub_apple, _ = SubCategory.objects.get_or_create(main_category=main_com, name='애플', order=2)
sub_hyundai, _ = SubCategory.objects.get_or_create(main_category=main_com, name='현대자동차', order=3)

sub_nj, _ = SubCategory.objects.get_or_create(main_category=main_mv, name='NewJeans', order=1)
sub_bts, _ = SubCategory.objects.get_or_create(main_category=main_mv, name='BTS', order=2)

sub_tiktok, _ = SubCategory.objects.get_or_create(main_category=main_shorts, name='TikTok 챌린지', order=1, is_vertical=True)
sub_insta, _ = SubCategory.objects.get_or_create(main_category=main_shorts, name='Instagram Reels', order=2, is_vertical=True)

print("Creating dummy works...")
dummy_works = [
    {
        'sub_category': sub_nike,
        'title': '나이키(Nike) 2026 캠페인',
        'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'content': '나이키의 새로운 글로벌 캠페인 영상입니다. 역동적인 움직임을 강조했습니다.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_apple,
        'title': '애플(Apple) 비전 프로 런칭',
        'youtube_link': 'https://www.youtube.com/watch?v=TX9qSaGXFyg',
        'content': '애플 비전 프로의 기능과 사용성을 보여주는 상업 영상.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_hyundai,
        'title': '현대자동차 아이오닉 6 글로벌 필름',
        'youtube_link': 'https://www.youtube.com/watch?v=GVhwXCAwcAA',
        'content': '미래 지향적인 디자인을 강조한 자동차 브랜드 필름.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_nj,
        'title': 'NewJeans (뉴진스) - Hype Boy Official MV',
        'youtube_link': 'https://www.youtube.com/watch?v=11cta61wi0g',
        'content': '청량한 색감과 다이내믹한 컷 편집이 돋보이는 뮤직비디오.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_bts,
        'title': 'BTS (방탄소년단) - Dynamite',
        'youtube_link': 'https://www.youtube.com/watch?v=gdZLi9oWNZg',
        'content': '레트로 컨셉을 세련되게 풀어낸 글로벌 아티스트 뮤직비디오.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_tiktok,
        'title': '[SHORTS] 르세라핌 안무 챌린지',
        'youtube_link': 'https://www.youtube.com/watch?v=mGjBIAfF178',
        'content': '세로형 포맷에 맞춘 트렌디한 숏폼 콘텐츠.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_insta,
        'title': '[SHORTS] 1분 만에 보는 스트릿 패션',
        'youtube_link': 'https://www.youtube.com/shorts/5v2jJ8eF-5A',
        'content': '빠른 템포의 편집과 감각적인 트랜지션이 들어간 패션 숏폼.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_nike,
        'title': '코카콜라(Coca-Cola) 짜릿한 여름 캠페인',
        'youtube_link': 'https://www.youtube.com/watch?v=7b9GZ08mGGE',
        'content': '여름의 청량함과 짜릿함을 담은 글로벌 브랜드 필름.',
        'status': 'COMPLETED',
        'is_visible': True,
    },
    {
        'sub_category': sub_apple,
        'title': '삼성전자 갤럭시 S26 언팩 하이라이트',
        'youtube_link': 'https://www.youtube.com/watch?v=5EqruEbMcO4',
        'content': '최신 기술과 혁신을 강조한 갤럭시 언팩 행사 하이라이트.',
        'status': 'COMPLETED',
        'is_visible': True,
    }
]

for w in dummy_works:
    Work.objects.create(**w)

print(f"Successfully created {len(dummy_works)} dummy works!")
