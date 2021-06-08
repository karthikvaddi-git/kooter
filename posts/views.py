from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from posts.models import *
from posts.forms import NewPostForm
from  django.http import HttpResponse,HttpResponseRedirect
from profiles.models import *
# Create your views here.



# Create your views here.
@login_required
def index(request):
	pro = profile.objects.filter(userprofile=request.user)
	user = request.user
	posts = user.stream_set.all()
	form = NewPostForm()
	group_ids = []

	for post in posts:
		group_ids.append(post.post_id)

	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
	context = {"post_items": post_items, "form": form, "pro": pro}
	return render(request, "index.html", context)


@login_required
def postupload(request):
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			content = request.FILES.get('content')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)

			p, created = Post.objects.get_or_create(caption=caption, user=user,content=content)
			p.tags.set(tags_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return redirect('index')


@login_required
def like(request, post_id):
	print("in liked post")
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return redirect('index')
