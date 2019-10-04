from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404

from .forms import CommentForm, TestForm, QuestionForm
from .models import Test


def get_posts_pages(request):
    search = request.GET.get('search', '')
    posts = Test.objects.filter(
        Q(name__icontains=search)
    ) if search \
        else Test.objects.all()

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return page


def get_comments_pages(request, comments):
    paginator = Paginator(comments, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return page


def get_pages_context(page):
    have_pages = page.has_other_pages()
    prev_url = '?page={}'.format(page.previous_page_number()) \
        if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) \
        if page.has_next() else ''

    return {
        'page': page,
        'have_pages': have_pages,
        'next_url': next_url,
        'prev_url': prev_url
    }


def show_tests(request):
    page = get_posts_pages(request)
    return render(request, 'tests/test_list.html', context=get_pages_context(page))


class ShowTest(View):
    def get(self, request, slug):
        test = get_object_or_404(Test, slug__iexact=slug)
        context = {
            'test': test,
            'form': CommentForm,
        }
        page = get_comments_pages(request, test.comment_set.all())
        context.update(get_pages_context(page))
        return render(request, 'tests/test_show.html', context=context)


class CreateTest(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tests/test_create.html', context={
            'form': TestForm(),
            'questions': QuestionForm()
        })

    def post(self, request):
        test = TestForm(request.POST)
        questions = QuestionForm(request.POST)
        if test.is_valid() and questions.is_valid():
            test = test.save(commit=False)
            test.author = request.user
            test.save()
            questions.save()
            return redirect(test.get_absolute_url())
        return render(request, 'tests/test_create.html', context={
            'form': test,
            'questions': questions
        })


class AddComment(View):
    def get(self, request, slug):
        raise Http404

    def post(self, request, slug):
        test = Test.objects.get(slug__iexact=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                test.comment_set.create(
                    author=request.user,
                    text=form.cleaned_data.get('text')
                )
            except Exception as e:
                return redirect(test.get_absolute_url())
        return redirect(test.get_absolute_url())