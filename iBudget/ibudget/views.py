"""
Views module for handling AWS S3
"""
from django.utils import datastructures
from django.http import HttpResponse, JsonResponse
from django.views import View
from utils.aws_helper import AwsService
from utils.response_helper import (RESPONSE_400_INVALID_DATA, RESPONSE_400_NO_FILE,
                                   RESPONSE_404_NOT_FOUND, RESPONSE_200_SUCCESS,
                                   RESPONSE_500_NO_SUCCESS, RESPONSE_400_UPLOAD_ERROR)


class FileHandler(View):
    """ View for handling CRUD methods for images in the AmazonS3 bucket
    """
    def get(self, request):
        """the method retrieves default icons from AWS S3
        :param - request object
        """
        if request.GET['tab'] == 'fund':
            urls = AwsService.get_default_list_icons('standard_fund/')[1:]
        elif request.GET['tab'] == 'income':
            urls = AwsService.get_default_list_icons('standard_income/')[1:]
        elif request.GET['tab'] == 'spending':
            urls = AwsService.get_default_list_icons('standard/')[1:]
        elif request.GET['tab'] == 'group':
            urls = AwsService.get_default_list_icons('standard_group/')[1:]
        return JsonResponse(urls, status=200, safe=False)



    def post(self, request):# pylint: disable=no-self-use
        """The name property of the file which is passed is 'icon', so in HTML form it must be set:
        <input type='file' name = 'icon'>
        """
        try:
            if request.FILES:
                pic = request.FILES['icon']
                while AwsService.check_if_in_bucket(pic) != True:
                    pic.name = AwsService.change_filename(pic)
                    # return RESPONSE_400_INVALID_DATA
                if AwsService.upload(pic):
                    pic = str(pic)
                    url = AwsService.get_image_url(pic)
                    return HttpResponse(url, status=201)
                return RESPONSE_500_NO_SUCCESS
            return RESPONSE_400_UPLOAD_ERROR
        except datastructures.MultiValueDictKeyError:
            return RESPONSE_400_NO_FILE


    def put(self, request):# pylint: disable=no-self-use
        """The method must accept the name of the file (string) of the image which is already used
        as a profile photo, and the new image which is passed in a form.
        The name property of the file which is passed is 'icon', the name of the file to be replaced
        is 'old', so in HTML form it must be set: <input type='file' name = 'icon'>
        """
        request.method = 'POST'
        req_dict = request.POST
        old_file = req_dict['old']
        new_file = request.FILES['icon']
        if AwsService.upload(new_file):
            if AwsService.del_photo(old_file):
                if not AwsService.check_if_in_bucket(new_file):
                    return RESPONSE_200_SUCCESS
            return RESPONSE_404_NOT_FOUND
        return RESPONSE_500_NO_SUCCESS


    def delete(self, request):# pylint: disable=no-self-use
        """the method must accept the name of the file (string) of the image which is already
         used as a profile photo or icon
         """
        key = request.body.decode()
        if not AwsService.check_if_in_bucket(key):
            if AwsService.del_photo(key):
                return RESPONSE_200_SUCCESS
            return RESPONSE_500_NO_SUCCESS
        return RESPONSE_404_NOT_FOUND
