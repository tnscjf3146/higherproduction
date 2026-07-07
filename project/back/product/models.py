from django.db import models

class PlanType(models.Model):
    name = models.CharField(max_length=255, verbose_name="플랜 종류 이름")
    def __str__(self): return self.name

class Recommend(models.Model):
    name = models.CharField(max_length=255, verbose_name="항목 이름")
    def __str__(self): return self.name

class Operation(models.Model):
    name = models.CharField(max_length=255, verbose_name="항목 이름")
    def __str__(self): return self.name

class Production(models.Model):
    name = models.CharField(max_length=255, verbose_name="항목 이름")
    def __str__(self): return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="항목 이름")
    def __str__(self): return self.name

class Plan(models.Model):
    plan_type = models.ForeignKey(PlanType, on_delete=models.SET_NULL, null=True, verbose_name="플랜 종류")
    name = models.CharField(max_length=255, verbose_name="플랜명 (ex: Basic Channel Operation)")
    subname = models.CharField(max_length=255, verbose_name="서브명 (ex: 베이직 채널 운영)", blank=True, null=True)
    price = models.IntegerField(verbose_name="가격(만원)")
    
    recommends = models.ManyToManyField(Recommend, blank=True, verbose_name="추천 대상")
    operations = models.ManyToManyField(Operation, blank=True, verbose_name="운영 목적")
    productions = models.ManyToManyField(Production, blank=True, verbose_name="촬영 / 편수")
    items = models.ManyToManyField(Item, blank=True, verbose_name="제작 항목")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        type_name = self.plan_type.name if self.plan_type else '미지정'
        return f"[{type_name}] {self.name}"
