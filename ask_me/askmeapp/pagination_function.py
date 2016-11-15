from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(data, howmany, page):
    paginator = Paginator(data, howmany) # Show howmany questions per page
    try:	
        paginated_data_list = paginator.page(page)
	pagenum = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
	pagenum = 1	
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_data_list = paginator.page(paginator.num_pages)
	pagenum = paginator.num_pages

    if pagenum >= 3:
		paginator.show_prev_prev = True
		paginator.prev_prev = pagenum - 2
    else:
		paginator.show_prev_prev = False
    if pagenum >= 4:
		paginator.show_gap_prev = True
    else: 	
		paginator.show_gap_prev = False

    if (pagenum + 2) <= paginator.num_pages :
		paginator.show_next_next = True
		paginator.next_next = pagenum + 2
    else:
		paginator.show_next_next = False
    if (pagenum + 3) <= paginator.num_pages :
		paginator.show_gap_next = True
    else: 	
		paginator.show_gap_next = False
    return paginated_data_list

