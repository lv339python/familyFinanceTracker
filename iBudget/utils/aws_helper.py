"""
File Handler
Provides methods for upload and download processes of the object to Amazon S3 service
"""
import boto3

from ibudget.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_STORAGE_BUCKET_NAME


class AwsService:
    """the class which handles actions with files on AWS
    """
    boto_resource = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    boto_bucket = boto_resource.Bucket(AWS_STORAGE_BUCKET_NAME)
    boto_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    @classmethod
    def check_if_in_bucket(cls, pic):
        """the method accept the name of the file(string) and checks if it exists
        in a bucket; returns boolean value
        """
        pic = str(pic)
        bucket_list = cls.boto_client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME)
        for obj in bucket_list['Contents']:
            if obj['Key'] == pic:
                return False
        return True

    @classmethod
    def upload(cls, pic):
        """the method which accepts the file and uploads it to the bucket
        """
        response = cls.boto_bucket.put_object(Key=pic.name, Body=pic.read())
        if response:
            return True
        return False

    @classmethod
    def get_image_url(cls, key):
        """the method accepts the name of the file(string), generates its
        URL and returns it
        """
        print(key)
        url = cls.boto_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': key
            }
        )
        for char in url:
            if char == '?':
                url = url[:url.index(char)]
        return url

    @classmethod
    def del_photo(cls, key):
        """the method  accepts the name of the file and deletes if from the bucket;
        returns boolean value
        """
        response = cls.boto_client.delete_object(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key=key,
        )
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status in (200, 204):
            return True
        return False

    @classmethod
    def get_default_list_icons(cls, tab):
        """the method accepts forms a list of dictionaries with the file names and their URLs from
        those available on Amazon S3
        """
        bucket_list = cls.boto_client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME)
        urls = [{"name": img["Key"],
                 "path": cls.get_image_url(img['Key'])} for img in bucket_list['Contents'] if
                img['Key'].startswith(tab)]
        return urls
