from django.db import models

def default_footer_slogan_main():
    return ["당신의 브랜드,", "한 단계 더 위로"]

def default_about_headings():
    return ["MISSION", "VISION", "CORE VALUES"]

class SiteSetting(models.Model):
    logo_kr = models.CharField(max_length=255, blank=True, null=True, verbose_name="국문 로고 텍스트/경로", default="국문 로고")
    logo_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="영문 로고 텍스트/경로", default="EN_LOGO")
    about_headings = models.JSONField(blank=True, null=True, verbose_name="About 섹션 제목 리스트", default=default_about_headings)
    email = models.EmailField(blank=True, null=True, verbose_name="스튜디오 이메일", default="email@gmail.com")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="스튜디오 전화번호", default="+82 10-0000-0000")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="스튜디오 주소", default="우리집")
    instagram_handle = models.CharField(max_length=100, blank=True, null=True, verbose_name="인스타그램 핸들", default="인스타핸들")
    instagram_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="인스타그램 주소", default="https://인스타_주소")
    
    # --- Service Section Config ---
    is_service_visible = models.BooleanField(default=True, verbose_name="Service 노출 여부")
    service_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Service 타이틀", default="MONTHLY PLAN")
    service_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="Service 서브설명", default="영상 운영 가격 / 한달 기준")
    
    # --- About Section Config ---
    is_about_visible = models.BooleanField(default=True, verbose_name="About 노출 여부")
    about_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="About 타이틀", default="ABOUT THE STUDIO")
    about_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="About 서브설명", default="하이어, 더 높은 곳으로")
    
    # --- Contact / Footer Section Config ---
    is_contact_visible = models.BooleanField(default=True, verbose_name="Contact 노출 여부")
    contact_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Contact 페이지 타이틀", default="LET'S GO HIGHER")
    contact_header_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Footer(Contact) 타이틀", default="GET IN TOUCH")
    contact_header_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="Footer(Contact) 서브설명", default="하이어, 더 높은 곳으로")
    
    footer_slogan_main = models.JSONField(blank=True, null=True, verbose_name="푸터 메인 슬로건", default=default_footer_slogan_main)
    footer_slogan_sub = models.CharField(max_length=255, blank=True, null=True, verbose_name="푸터 서브 슬로건", default="Let's go higher.")

    class Meta:
        verbose_name = "사이트 설정"
        verbose_name_plural = "사이트 설정"

    def __str__(self):
        return "Site Settings"
