from django import forms
from django.forms import ModelForm, Textarea
from .models import Blog, Category, Comment


class BlogForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['title'].widget.attrs.update({'id': 'title'})
        self.fields['category'].empty_label = None
        self.fields['category'].widget.choices = self.fields['category'].choices
        self.fields['edited'].widget.attrs['readonly'] = True
        self.fields['edited'].widget.attrs.update({'id': 'formfieldastext'})

    class Meta:
        model = Blog
        fields = ('title', 'body', 'category', 'published', 'edited', )
        labels = {
            'title': '',
            'body': '',
            'category': 'Category',
        }
        widgets = {
            'body': Textarea(attrs={'cols': 200, 'rows': 20}),
        }


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})

    class Meta:
        model = Category
        fields = ('title', )
        labels = {
            'title': 'title',
        }

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'placeholder': 'Comment'})

    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {
            'comment': '',
        }
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 6}),
        }

class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search', max_length=100)
