"""
Response helper
Module that provides various HttResponse objects for project.
"""
from django.http import HttpResponse

RESPONSE_400_INVALID_DATA = HttpResponse('the file with such a name already exists, please change'
                                         ' the file name'
                                         ' and upload again', status=400)

RESPONSE_400_NO_FILE = HttpResponse('You did not provide any file to upload. Please choose a'
                                    'file and try again', status=400)
RESPONSE_404_NOT_FOUND = HttpResponse('Invalid file name or file is already deleted', status=404)

RESPONSE_200_SUCCESS = HttpResponse('The file was successfully updated/deleted', status=200)

RESPONSE_500_NO_SUCCESS = HttpResponse('The file removal/upload was not successful, internal server'
                                       ' error',
                                       status=500)

RESPONSE_400_UPLOAD_ERROR = HttpResponse('The file was not successfully uploaded to the server.',
                                         status=400)
