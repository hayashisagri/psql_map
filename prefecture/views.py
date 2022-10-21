import copy
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from prefecture.consts import NUM_ALL_PREFECTURES
from prefecture.forms import ReviewForm
from prefecture.models import PREFECTURES_CODE, Prefecture, Review
from prefecture.serializers import PrefectureSerializer


class HomeView(TemplateView):
    template_name = "prefecture/home.html"


class DetailPrefectureView(LoginRequiredMixin, DetailView):
    template_name = "prefecture/prefecture_detail.html"
    model = Prefecture


class ResisterPrefectureView(LoginRequiredMixin, CreateView):
    template_name = "prefecture/prefecture_register.html"
    model = Prefecture
    fields = ("name",)
    success_url = reverse_lazy("mypage")

    def form_valid(self, form):
        form.instance.user = self.request.user

        visited_list = Prefecture.objects.filter(user=self.request.user)
        for vl in visited_list:
            if str(vl) == form.instance.name:
                return render(
                    self.request,
                    "prefecture/prefecture_register.html",
                    {"error": "すでに登録済みの都道府県です。"},
                )

        return super().form_valid(form)


class DeletePrefectureView(LoginRequiredMixin, DeleteView):
    template_name = "prefecture/prefecture_confirm_delete.html"
    model = Prefecture
    success_url = reverse_lazy("mypage")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "prefecture/review_form.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prefecture"] = Prefecture.objects.get(
            pk=self.kwargs["prefecture_id"]
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not bool(form.instance.image):
            form.instance.image = "no_image.png"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "prefecture-detail", kwargs={"pk": self.object.prefecture.id}
        )


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ("title", "text", "rate", "image")
    template_name = "prefecture/review_update.html"

    def get_success_url(self):
        return reverse(
            "prefecture-detail", kwargs={"pk": self.object.prefecture.id}
        )


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    template_name = "prefecture/review_confirm_delete.html"
    model = Review

    def get_success_url(self):
        return reverse(
            "prefecture-detail", kwargs={"pk": self.object.prefecture.id}
        )


def root_view(request):
    return redirect('home')


@login_required
def mypage_view(request):
    visited_list = Prefecture.objects.filter(user=request.user)
    visited_count = len(visited_list)
    un_visited_count = NUM_ALL_PREFECTURES - visited_count
    copied_prefs = copy.deepcopy(PREFECTURES_CODE)

    un_visited_list = []  # 未訪問の都道府県リスト
    visit_dict = {}  # ポリゴン表示用、jsに渡す用
    for p in copied_prefs:
        un_visited_list.append(p[1])
        visit_dict[p[0]] = p[1]

    for vl in visited_list:
        un_visited_list.remove(str(vl))
        for i in range(1, NUM_ALL_PREFECTURES):
            i_str = str(i)
            if str(vl) == visit_dict[i_str]:
                visit_dict[i_str] = 1

    for i in range(1, NUM_ALL_PREFECTURES):
        i_str = str(i)
        if visit_dict[i_str] != 1:
            visit_dict[i_str] = 0

    prefecture_colour_data = json.dumps(visit_dict)

    return render(
        request,
        "prefecture/mypage.html",
        {
            "visited_list": visited_list,
            "visited_count": visited_count,
            "un_visited_list": un_visited_list,
            "un_visited_count": un_visited_count,
            "prefecture_colour_data": prefecture_colour_data,
        },
    )


@api_view(['GET'])
def prefecture_list(request):
    prefectures = Prefecture.objects.filter(user=request.user)
    serializer = PrefectureSerializer(prefectures, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    else:
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
