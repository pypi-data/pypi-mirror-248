import base64
import csv
import glob
import hashlib
import json
import os
import uuid
from io import BytesIO
from multiprocessing.pool import ThreadPool

import pandas as pd
import boto3
from PIL import Image, ImageOps
import requests
from botocore.exceptions import ClientError
from django.utils.text import slugify

from tasq_cli import credentials
from tasq_cli.db import UploadsDatabase
from tasq_cli.server import make_request

# from utils import timestamp_for_file_name

logger = None


def upload_file(dataset_name, db, settings, client, file_name_with_path, leaf_path):
    file_path, file_name = os.path.split(file_name_with_path)
    relative_file_path = f'{leaf_path}{file_path.split(leaf_path)[-1]}'.replace('-', '_')
    ext = file_name.split('.')[-1]

    object_name = f'client_{credentials.CLIENT_ID}/{relative_file_path}/{uuid.uuid4().hex}.{ext}'
    logger.debug(f'Checking if file needs to be uploaded ...')

    # before upload check if file exists on server under this dataset
    with open(f'{file_path}/{file_name}', 'rb') as infile:
        image_wrapper = BytesIO()
        # if file is png, jpg, or jpeg - rotate
        if ext in ['png', 'jpg', 'jpeg']:
            try:
                image = Image.open(infile)
                # Remove alpha channel for JPEG images
                if ext in ['jpg', 'jpeg']:
                    image = image.convert('RGB')

                transposed_image = ImageOps.exif_transpose(image)
                transposed_image.save(image_wrapper, ('JPEG' if ext == 'jpg' else ext))
            except:
                logger.info('Possible corrupted image, failed transposing it.')
                logger.info(f'Offending file: {file_path}/{file_name}')
        else:
            image_wrapper = infile

        md5 = hashlib.md5(image_wrapper.getvalue() if 'getvalue' in dir(image_wrapper) else image_wrapper.read())
        image_wrapper.seek(0)
        content_md5 = base64.b64encode(md5.digest()).decode('utf-8')
        md5_hash = md5.hexdigest()

        logger.debug(f'File hash: {md5_hash}')
        uploaded_entry = db.get_upload(dataset_name, md5_hash)

        bucket_name = settings.BUCKET if hasattr(settings, 'BUCKET') else credentials.BUCKET
        if uploaded_entry:
            logger.info(f'File with hash {md5_hash} is already uploaded to dataset {dataset_name}.')
            upload_entry = {
                'bucket': bucket_name,
                'dataset_name': dataset_name,
                'file_name': f'{relative_file_path}/{file_name}',
                'object_name': uploaded_entry['object_name'],
                'md5_hash': md5_hash,
                'url': uploaded_entry['URL'],
                'cdn_url': settings.CDN_URL.format(object_name=uploaded_entry['object_name']),
            }
            return upload_entry

        if not settings.dry:
            logger.info(f'Uploading {file_name_with_path} to {bucket_name} as {object_name}.')
        else:
            logger.info(f'Dry running {file_name_with_path} to {bucket_name} as {object_name}. Nothing will be uploaded.')
        try:
            upload_entry = {
                'bucket': bucket_name,
                'dataset_name': dataset_name,
                'file_name': f'{relative_file_path}/{file_name}',
                'object_name': object_name,
                'md5_hash': md5_hash,
                'url': f'https://{bucket_name}.s3.amazonaws.com/{object_name}',
                'cdn_url': settings.CDN_URL.format(object_name=object_name),
            }
            if not settings.dry:
                if ext in ['pdf']:
                    response = client.put_object(
                        Body=image_wrapper,
                        Bucket=bucket_name,
                        Key=object_name,
                        ContentMD5=content_md5,
                        ContentType=f"application/{ext}",
                        ContentDisposition="inline",
                    )
                else:
                    response = client.put_object(
                        Body=image_wrapper,
                        Bucket=bucket_name,
                        Key=object_name,
                        ContentMD5=content_md5,
                        # see above ToDo
                    )
                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response['ETag'] == f'"{md5_hash}"':
                    tag_response = client.put_object_tagging(
                        Bucket=bucket_name,
                        Key=object_name,
                        Tagging={
                            'TagSet': [
                                {
                                    'Key': 'original_name',
                                    'Value': slugify(file_name),
                                },
                            ]
                        },
                    )

                    return upload_entry
                else:
                    logger.error(response)
            else:
                return upload_entry
        except ClientError as e:
            logger.error(e)


def get_files(dir_path, excluded_extensions):
    files = []
    logger.info(excluded_extensions)
    if len(excluded_extensions) > 1:
        glob_ending = f'!(**.{"|**.".join(excluded_extensions)})'
    else:
        glob_ending = '**'
    # files.extend(glob.glob(f'{dir_path}/{glob_ending}', recursive=True))
    # NOTE
    # The above glob patterns excludes things when run with ls in bash,
    # but for some reason it won't work through python. Check it out by uncommenting:
    #
    # logger.info(f'ls {dir_path}/{glob_ending}')
    #
    # That is why we run a dumb glob and a list comprehension to exclude all
    # the files we don't like.
    files.extend(glob.glob(f'{dir_path}/**', recursive=True))
    filtered_files = [f for f in files if (f.split('.')[-1] not in excluded_extensions) and not os.path.isdir(f)]

    return filtered_files


def do_upload(dataset_name, search_path, exclude, settings):
    global logger
    logger = settings.get_logger()
    if exclude:
        if len(exclude) > 0:
            excluded_extensions = [ext[0] for ext in exclude]
    else:
        excluded_extensions = []

    client = boto3.client(
        's3',
        aws_access_key_id=credentials.ACCESS_KEY,
        aws_secret_access_key=credentials.SECRET_KEY,
    )

    logger.info(f'Using access key {credentials.ACCESS_KEY[:3]}*********{credentials.ACCESS_KEY[-3:]} '
                f'and secret {credentials.SECRET_KEY[:3]}*********{credentials.SECRET_KEY[-3:]}.')

    leaf_path = os.path.basename(os.path.normpath(search_path))
    added_files = []

    files = get_files(search_path, excluded_extensions)
    num_files = len(files)
    logger.info(f'Found {num_files} files.')

    def single_upload(file_name):
        db = UploadsDatabase()
        upload_entry = upload_file(dataset_name, db, settings, client, file_name, leaf_path)
        if not upload_entry:
            db.close()
            exit(1)
        else:
            added_files.append(upload_entry)
            if not settings.dry:
                db.insert_upload(**upload_entry)
        db.close()

    pool = ThreadPool(processes=10)
    pool.map(single_upload, files)

    # write out image urls to csv
    os.makedirs("./out/", exist_ok=True)

    csv_rows = [
        [
            settings.CDN_URL.format(object_name=uploaded_entry['object_name']),  # object_name
            json.dumps({'file_name': uploaded_entry['file_name']}),  # object
            # uploaded_entry['file_name'], # file_name
        ]
        for uploaded_entry in added_files
    ]

    # NOTE
    # the csv output used to contain a full timestamp
    # with open(f'./out/{dataset_name}_{timestamp_for_file_name()}.csv', 'w') as csvfile:
    with open(f'./out/{dataset_name}.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='unix')
        csvwriter.writerows(csv_rows)


def create_csv_from_currently_uploaded_files(dataset_name, file_name, settings):
    db = UploadsDatabase()
    global logger
    logger = settings.get_logger()

    if not dataset_name:
        if not file_name:
            logger.error('No dataset_name or example file_name was provided.')
            return
        res = get_dataset_name(db, file_name)
        if not res:
            logger.error('No such file was uploaded.')
            return
        dataset_name = res[0]

    entries = db.get_uploaded_files_by_dataset_name(dataset_name)
    row_values = {'file_name': 0, 'cdn_url': 1}
    csv_rows = [
        [
            entry[row_values['cdn_url']],
            json.dumps({'file_name': entry[row_values['file_name']]}),  # object
        ]
        for entry in entries
    ]
    if not os.path.exists('./out/'):
        os.makedirs('./out')
    with open(f'./out/{dataset_name}.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='unix')
        csvwriter.writerows(csv_rows)


def get_dataset_name(db, file_name):
    file_path, file_name = os.path.split(file_name)
    leaf_path = os.path.basename(os.path.normpath(file_path))
    relative_file_path = f'{leaf_path}{file_path.split(leaf_path)[-1]}'.replace('-', '_')
    res = db.get_dataset_name_by_filename(f'{relative_file_path}/{file_name}')
    return res


def upload_csv(path, project_id, tag=None):
    headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/vnd.api+json'}
    file_name = path.split('/')[-1]
    pre_signed_url = json.loads(make_request(f"/presigned_uploads/presigned_url?file_name={file_name}", headers=headers).content.decode())
    with open(path, 'rb') as file:
        files = {'file': (path, file)}
        s3_response = requests.post(pre_signed_url['url'], data=pre_signed_url['fields'], files=files)
    s3_file_name = s3_response.headers['location'].split('/')[-1]
    file_upload_payload = {
        "data": {
            "type": "genericFiles",
            "attributes": {
                "fileName": f"{s3_file_name}",
                "originalFilename": f"{file_name}",
            }
        }
    }
    uploaded_file_response = make_request('/presigned_uploads', json=file_upload_payload, headers=headers)
    source_file_id = json.loads(uploaded_file_response.content.decode())['data']['id']
    dataset_response = make_request(f'/projects/{project_id}')
    dataset_id = dataset_response.json()['data']['relationships']['dataset']['data']['id']
    source_file_payload = {
        "data": {
            "type": "sourceFiles",
            "attributes": {
                "file": {
                    "type": "GenericFile",
                    "id": f"{source_file_id}",
                },
                "dataset": {
                    "type": "datasets",
                    "id": dataset_id,
                },
            },
        }
    }
    if tag:
        source_file_payload['data']['attributes']['tag_name'] = tag
    r = make_request('/source_files', json=source_file_payload, headers=headers)
    return json.loads(r.content.decode())['data']["id"]


def upload_array(array, project_id, file_name, tag=None):
    headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/vnd.api+json'}
    pre_signed_url = json.loads(make_request(f"/presigned_uploads/presigned_url?file_name={file_name}", headers=headers).content.decode())

    df = pd.DataFrame(array).to_csv(None, index=False, header=False)

    files = {'file': df}
    s3_response = requests.post(pre_signed_url['url'], data=pre_signed_url['fields'], files=files)
    s3_file_name = s3_response.headers['location'].split('/')[-1]
    print(s3_file_name)
    file_upload_payload = {
        "data": {
            "type": "genericFiles",
            "attributes": {
                "fileName": f"{s3_file_name}",
                "originalFilename": f"{file_name}",
            },
        }
    }
    uploaded_file_response = make_request('/presigned_uploads', json=file_upload_payload, headers=headers)
    source_file_id = json.loads(uploaded_file_response.content.decode())['data']['id']
    dataset_response = make_request(f'/projects/{project_id}')
    dataset_id = dataset_response.json()['data']['attributes']['datasetId']
    source_file_payload = {
        "data": {
            "type": "sourceFiles",
            "attributes": {
                "file": {
                    "type": "GenericFile",
                    "id": f"{source_file_id}",
                },
                "dataset": {
                    "type": "datasets",
                    "id": dataset_id,
                },
            },
        }
    }
    if tag:
        source_file_payload['data']['attributes']['tag_name'] = tag
    r = make_request('/source_files', json=source_file_payload, headers=headers)
    return json.loads(r.content.decode())['data']["id"]


if __name__ == '__main__':
    pass
