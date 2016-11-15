from django.core.mypaginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(data, howmany, page):
    paginator = Paginator(data, howmany, page) # Show howmany questions per page
    try:	
        paginated_data_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_data_list = paginator.page(paginator.num_pages)
    return paginated_data_list
