from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Tag, Comment, CustomUser
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("Access denied. User must be an admin.")
    return wrapper
@admin_only
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the current user as the author
            post.save()
            form.save_m2m()  # Save any many-to-many relationships if there are any

            # Redirect to the detail view of the newly created post
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form, 'api_key': settings.API_KEY})
# Create your views here.


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    tech_posts = Post.objects.filter(categories__name="Technology")
    prod_posts = Post.objects.filter(categories__name="Productivity")
    insp_posts = Post.objects.filter(categories__name="Inspiration")
    return render(
        request,
        "index.html",
        {
            "tech_posts": tech_posts,
            "posts": posts,
            "prod_posts": prod_posts,
            "insp_posts": insp_posts,
        },
    )


def postdetail(request, pk):
    posts = Post.objects.all()
    post = get_object_or_404(Post, id=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    profile_avatar = CustomUser.objects.filter(
        user=post.author).values('avatar').first()

    if request.method == "POST":
        comment_text = request.POST.get("comment")
        user = request.user
        parent_id = request.POST.get("parent_id")

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
        Comment.objects.create(comment=comment_text,
                               user=user, post=post, parent=parent_comment)
        return redirect('post_detail', pk=pk)

    comments = post.comment_set.filter(parent__isnull=True)

    if post.views is None:
        post.views = 0
    post.views += 1
    post.save()

    popular_post = Post.objects.all().order_by("-views")
    more_post = Post.objects.filter(categories__in=post.categories.all())

    context = {
        "post": post,
        "more_post": more_post,
        "popular_post": popular_post,
        "posts": posts,
        "categories": categories,
        "tags": tags,
        "comments": comments,
        "profile_avatar": profile_avatar,

    }

    return render(request, "post_detail.html", context)


def category(request, pk):
    posts = Post.objects.all()
    category_posts = Post.objects.filter(categories__name=pk)
    popular_post = Post.objects.all().order_by("-views")
    categories = Category.objects.all()
    tags = Tag.objects.all()

    paginator = Paginator(category_posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "popular_post": popular_post,
        "page_obj": page_obj,
        "pk": pk,
        "categories": categories,
        "tags": tags,
    }

    return render(request, "category.html", context)


def searchresult(request):
    posts = Post.objects.all()
    popular_post = Post.objects.all().order_by("-views")
    categories = Category.objects.all()
    tags = Tag.objects.all()
    q = request.GET.get("q")
    if q:
        search_posts = Post.objects.filter(
            Q(title__icontains=q)
            | Q(content__icontains=q)
            | Q(categories__name__icontains=q)
            | Q(tags__name__icontains=q)
        ).distinct()
    else:
        search_posts = Post.objects.none()

    paginator = Paginator(search_posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "q": q,
        "popular_post": popular_post,
        "page_obj": page_obj,
        "categories": categories,
        "tags": tags,
    }

    return render(request, "search_result.html", context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'sign_in.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully signed in.')
            # Redirect to the index page after successful login.
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'sign_in.html')


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        avatar = request.FILES.get('avatar')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()

            user_profile = CustomUser(user=user, avatar=avatar)
            user_profile.save()

            return redirect('sign_in')

    return render(request, 'sign_up.html')


def sign_out(request):
    logout(request)
    return redirect('index')
