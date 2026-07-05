import os
import sys
import django
import random

# 프로젝트 루트 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from work.models import Category, Work
from django.contrib.auth import get_user_model

User = get_user_model()

def populate_works():
    print("기존 데이터 삭제 중...")
    Category.objects.all().delete()
    Work.objects.all().delete()
    
    # 1. 카테고리 생성 (가로 2개, 세로 1개)
    cat_cf = Category.objects.create(name="브랜드 필름", order=1, is_vertical=False)
    cat_mv = Category.objects.create(name="뮤직비디오", order=2, is_vertical=False)
    cat_shorts = Category.objects.create(name="유튜브 쇼츠 / 릴스", order=3, is_vertical=True)
    
    # 2. 더미 유튜브 링크 (가로형)
    horizontal_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "https://www.youtube.com/watch?v=JGwWNGJdvx8",
        "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
    ]
    
    # 3. 더미 유튜브 링크 (세로형 쇼츠)
    vertical_links = [
        "https://www.youtube.com/shorts/51Qx0_n1t5g",
        "https://www.youtube.com/shorts/3fVfKz_7q1o",
        "https://www.youtube.com/shorts/aH2l-H-R_eQ",
        "https://www.youtube.com/shorts/B_Zqg7k4WfM",
        "https://www.youtube.com/shorts/6-zC2sQW8cI"
    ]
    
    def create_dummy_works(category, prefix, count, link_pool):
        print(f"[{category.name}] 영상 {count}개 생성 중...")
        for i in range(1, count + 1):
            Work.objects.create(
                category=category,
                user=None,
                title=f"{prefix} 영상 #{i:02d}",
                youtube_link=random.choice(link_pool),
                content=f"{prefix} 더미 설명입니다. {i}번째 영상.",
                status='COMPLETED',
                is_visible=True
            )
            
    # 각각 20개씩 생성 (ALL 탭과 카테고리 탭에서 페이지네이션 확인용)
    create_dummy_works(cat_cf, "브랜드 필름", 20, horizontal_links)
    create_dummy_works(cat_mv, "뮤직비디오", 20, horizontal_links)
    create_dummy_works(cat_shorts, "세로형 숏폼", 20, vertical_links)
    
    print("더미 데이터 생성이 완료되었습니다!")

if __name__ == "__main__":
    populate_works()
