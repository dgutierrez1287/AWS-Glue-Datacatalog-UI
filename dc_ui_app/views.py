from django.shortcuts import render, redirect
from .lib.databases import get_all_databases
from .lib.tables import get_table_count, get_page_of_tables, get_table
import math
import logging

logger = logging.getLogger(__name__)

def index(request):

    dbs = get_all_databases()

    return render(request, 'index.html', {'dbs':dbs})


def table_list(request):

    db_name = request.GET['db']
        
    table_count = get_table_count(db_name)
    num_of_pages = math.ceil(table_count / 50)

    if table_count > 50:
        response = redirect(f'/tables/paged?db={db_name}&num_pages={num_of_pages}&page=1')
        return response

    return render(request, 'table_list.html', {'db_name': db_name})


def table_list_paged(request):

    db_name = request.GET['db']
    num_of_pages = int(request.GET['num_pages'])
    page_num = int(request.GET['page'])

    pages = []
    
    for p in range(num_of_pages):
        pages.append(p + 1)
        
    tables = get_page_of_tables(db_name, page_num, 50)

    prev_page = page_num - 1
    next_page = page_num + 1

    context_dict = {
        'db_name': db_name, 
        'paging': 'yes', 
        'pages': pages,
        'num_of_pages': num_of_pages,
        'tables': tables,
        'last_page': num_of_pages,
        'page_num': page_num,
        'prev_page': prev_page,
        'next_page': next_page,
    }

    logger.debug(f"context: {context_dict}")

    return render(request, 'table_list.html', context_dict)

def column_list(request):

    db_name = request.GET['db']
    table_name = request.GET['table']

    table = get_table(db_name, table_name)

    column_count = len(table.columns)

    paging = 'no'
    if column_count > 50:
        paging = 'yes'
        num_of_pages = math.ceil(column_count / 50)
        response = redirect(f'/table-view/paged?db={db_name}&table={table_name}&num_pages={num_of_pages}&page=1')
        return response

    context_dict = {
        'db_name': db_name,
        'table_name': table_name,
        'table_update_time': table.update_time,
        'table_description': table.description,
        'columns': table.columns
    }

    return render(request, 'table_view.html', context_dict)

def column_list_paged(request):

    db_name = request.GET['db']
    table_name = request.GET['table']
    num_of_pages = int(request.GET['num_pages'])
    page_num = int(request.GET['page'])

    table = get_table(db_name, table_name)

    column_count = len(table.columns)

    ending_count = page_num * 50
    starting_count = ending_count - 50

    paged_columns = table.columns[starting_count:ending_count]

    pages = []

    for p in range(num_of_pages):
        pages.append(p + 1)

    prev_page = page_num - 1
    next_page = page_num + 1

    
    context_dict = {
        'db_name': db_name,
        'table_name': table_name,
        'table_update_time': table.update_time,
        'table_description': table.description,
        'columns': paged_columns,
        'paging': 'yes',
        'pages': pages,
        'num_of_pages': num_of_pages,
        'last_page': num_of_pages,
        'page_num': page_num,
        'prev_page': prev_page,
        'next_page': next_page
    }

    logger.debug(f"context: {context_dict}")

    return render(request, 'table_view.html', context_dict)
