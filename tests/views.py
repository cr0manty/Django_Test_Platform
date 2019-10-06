from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Test, Question
from .forms import CommentForm, TestForm, QuestionForm


def get_pages(request):
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


def get_pages_context(page, filter_test=False):
    have_pages = page.has_other_pages()
    prev_url = '?page={}'.format(page.previous_page_number()) \
        if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) \
        if page.has_next() else ''

    return {
        'page': page,
        'have_pages': have_pages,
        'next_url': next_url,
        'prev_url': prev_url,
        'filter': filter_test
    }


def show_tests(request):
    page = get_pages(request)
    return render(request, 'tests/test_list.html', context=get_pages_context(page))


def show_filter_tests(request):
    page = get_pages(request)
    return render(request, 'tests/test_list.html', context=get_pages_context(page, True))


class ShowTest(View):
    def get(self, request, slug):
        test = get_object_or_404(Test, slug__iexact=slug)
        context = {
            'test': test,
            'form': CommentForm(),
            'question': QuestionForm()
        }
        page = get_comments_pages(request, test.comment_set.all())
        context.update(get_pages_context(page))
        return render(request, 'tests/test_show.html', context=context)

    def post(self, request, slug):
        question = QuestionForm(request.POST)
        test = get_object_or_404(Test, slug__iexact=slug)
        if question.is_valid() and test is not None:
            quest_old = Question.objects.filter(
                Q(question=question.cleaned_data.get('question')) &
                Q(test__id=test.id)).first()
            if quest_old is None:
                test.question_set.create(
                    question=question.cleaned_data.get('question'),
                    answers=question.get_answers(),
                    correct='answer_' + request.POST.get('answer')
                )
        context = {
            'test': test,
            'question': QuestionForm()
        }
        page = get_comments_pages(request, test.comment_set.all())
        context.update(get_pages_context(page))
        return render(request, 'tests/test_show.html', context=context)


class CreateTest(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tests/test_create.html', context={
            'form': TestForm(),
        })

    def post(self, request):
        test = TestForm(request.POST)
        if test.is_valid():
            test = test.save(commit=False)
            test.author = request.user
            test.save()
            return redirect(test.get_absolute_url())
        return render(request, 'tests/test_create.html', context={
            'form': test,
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
