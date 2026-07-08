import os
import django
from django.core.management import call_command

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def export_database():
    # 경로 설정
    # __file__은 현재 스크립트(back/export_db.py)의 절대 경로를 나타냅니다.
    back_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(back_dir) # project 폴더
    database_dir = os.path.join(project_dir, 'database')
    
    # database 폴더가 없으면 생성
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        print(f"[{database_dir}] 폴더를 생성했습니다.")
        
    output_file = os.path.join(database_dir, 'db_dump.json')
    
    # dumpdata 명령어를 실행하여 json 파일로 출력
    print(f"데이터베이스를 {output_file} 파일로 내보내는 중...")
    with open(output_file, 'w', encoding='utf-8') as f:
        # 모든 데이터를 json 형식으로 들여쓰기(indent) 4칸을 적용하여 추출합니다.
        call_command('dumpdata', format='json', indent=4, stdout=f)
        
    print("✅ 데이터베이스 JSON 백업이 성공적으로 완료되었습니다!")

if __name__ == '__main__':
    export_database()
