import django_filters
from django_filters import CharFilter

from django import forms

from .models import *

class PostFilter(django_filters.FilterSet):
	headline = CharFilter(field_name='headline', lookup_expr="icontains", label='Tiêu đề')

	class Meta:
		model = Post
		fields = ['headline']
class THPTFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr="icontains", label='Tên trường')
	khoihoc = django_filters.ChoiceFilter(field_name='khoihoc', choices=[('Toán', 'Toán'), ('Anh', 'Anh'), ('Văn', 'Văn'), ('Tin học','Tin học'), ('Lý','Lý'), ('Hóa','Hóa'), ('Sinh','Sinh'), ('Sử','Sử'), ('Địa','Địa')],lookup_expr="icontains", label='Môn chuyên')
	class Meta:
		model = XetDiemChuyen
		fields = ['khoihoc','name']
class Nonfilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr="icontains", label='Tên trường')
	class Meta:
		model = XetDiemChuyen
		fields = ['name']
class DienDanFilter(django_filters.FilterSet):
	headline = CharFilter(field_name='headline', lookup_expr="icontains", label='Tiêu đề')

	class Meta:
		model = DienDan
		fields = ['headline']