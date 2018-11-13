"""
This module consists functions for providing history boot files
"""
import io
from datetime import timedelta, date
from django.http import StreamingHttpResponse
from django.utils.dateparse import parse_datetime, parse_date
import xlsxwriter

def creating_empty_xlsx_file():
    """
    Function for creating empty xlsx file
    Returns:
        output: byte object
        workbook: xlsx empty workbook
        worksheet: created history worksheet
        formats dicts: dicts with cell formats
    """
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('history')

    formats_dict = dict()
    formats_dict['head_format'] = workbook.add_format\
        ({'bold': True, 'font_size': 12, 'align': 'center', 'border': 5})
    formats_dict['value_format'] = workbook.add_format\
        ({'num_format': '$#.#0', 'align': 'center', 'border': 1})
    formats_dict['date_format'] = workbook.add_format\
        ({'num_format': 'mmmm d yyyy', 'align': 'center', 'border': 1})
    formats_dict['cell_format'] = workbook.add_format({'align': 'center', 'border': 1})
    worksheet.set_column(0, 5, 20)

    return output, worksheet, workbook, formats_dict

def file_streaming_response(content_type, filename, output):
    """
    Function for creating empty xlsx file
    Args:
        output: byte object
        content_type: specific type for response file
        filename
    Returns:
        response
    """
    output.seek(0)

    response = StreamingHttpResponse(
        output,
        content_type=content_type
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def income_date_parser(request):
    """
    Function for parsing income date data from request
    Args:
        request
    Returns:
        date_dict: dictionary with date and user info
    """
    date_dict = dict()
    date_dict['user_id'] = request.user
    date_dict['start_date'] = parse_datetime(request.GET['start_date'])
    date_dict['finish_date'] = parse_datetime(request.GET['finish_date'])
    date_dict['utc_difference'] = timedelta(hours=int(request.GET['UTC']))

    return date_dict


def spending_date_parser(request):
    """
    Function for parsing and validation spending date data from request
    Args:
        request
    Returns:
        date_dict: dictionary with date and user info
    """
    date_dict = dict()
    date_dict['user_id'] = request.user
    date_dict['start_date'] = parse_date(request.GET['start_date'])
    date_dict['finish_date'] = parse_date(request.GET['finish_date'])
    date_dict['utc_difference'] = int(request.GET['UTC'])

    if not date_dict['start_date']:
        date_dict['start_date'] = date(date.today().year, date.today().month, 1)
    if not date_dict['finish_date']:
        date_dict['finish_date'] = date.today()
        date_dict['start_date'] = date_dict['start_date'] - timedelta\
            (hours=date_dict['utc_difference'])
    if date_dict['start_date'] > date_dict['finish_date']:
        date_dict['start_date'] = date_dict['finish_date']

    return date_dict
