import json
import os
from subprocess import PIPE, Popen
from typing import List

import pytest


"""
For all tests user string must exist with API key of stringstring
"""


async def add_test(url: str, images: List[str], permission: str) -> None:
    """
    all of the mock images are jpeg
    """
    # os.popen opens a pipe in the command line and is useful to store the result of the command
    curl_base = f"""
    curl -X 'POST' \
    '{url}' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    """

    for image in images:
        curl_base += f" -F 'images_upload=@mock-data/{image};type=image/jpeg'"
    print(curl_base)
    p = Popen(curl_base, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert 'images_uploaded' in json.loads(
        stdout) and f'total_{permission}' in json.loads(stdout)


@pytest.mark.asyncio
async def test_add_single_private():
    await add_test("http://127.0.0.1:8000/add/private/?api_key=stringstring&t=string",
                   ["test.jpg"], "private")


@pytest.mark.asyncio
async def test_add_bulk_public():
    await add_test("http://127.0.0.1:8000/add/public/?api_key=stringstring&t=string&t=string",
                   ["test.jpg", "test1.jpg"], "public")


@pytest.mark.asyncio
async def test_upload_images_matches_not_t():
    p = Popen("""
    curl -X 'POST' \
    'http://127.0.0.1:8000/add/private/?api_key=stringstring&t=string&t=string' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'images_upload=@mock-data/test.jpg;type=image/jpeg'
    """, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    # converting bytes of strings into JSON
    assert json.loads(stdout) == {
        "detail": "Please make sure the number of images match with your specified image properties"}


@pytest.mark.asyncio
async def test_invalid_image():
    p = Popen("""
    curl -X 'POST' \
    'http://127.0.0.1:8000/add/private/?api_key=stringstring&t=string' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'images_upload=@mock-data/test.pdf;type=application/pdf'
    """, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    # converting bytes of strings into JSON
    assert json.loads(stdout) == {
        "detail": "Please make sure that your images have any extension of the following: png, jpeg"}
