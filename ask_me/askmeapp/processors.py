from askmeapp.models import *


def right_block(request):
	popular_tags = Tag.objects.get_popular_tags()
	return {'popular_tags' : popular_tags}
