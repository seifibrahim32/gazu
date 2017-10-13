import functools
import requests
import json

from cachecontrol import CacheControlAdapter
from cachecontrol.heuristics import ExpiresAfter

from .encoder import CustomJSONEncoder

from .exception import (
    RouteNotFoundException,
    ServerErrorException,
    NotAuthenticatedException,
    NotAllowedException
)

# Little hack to allow json encoder to manage dates.
requests.models.complexjson.dumps = functools.partial(
    json.dumps,
    cls=CustomJSONEncoder
)

requests_session = requests.Session()


HOST = "http://pipeline-server.unit.local/"
tokens = {
    "access_token": "",
    "refresh_token": ""
}


def host_is_up():
    """
    :return: True if the host is up
    """
    response = requests_session.head(HOST)
    return response.status_code == 200


def set_cache_expiration_delay(seconds):
    """
    Set a cache for requests with a given expiration time.
    """
    adapter = CacheControlAdapter(
        heuristic=ExpiresAfter(seconds=seconds)
    )
    session.mount('http://', adapter)
    return session


def get_host():
    """
    Return host on which requests_session are sent.
    """
    return HOST


def set_host(new_host):
    """
    Get currently configured host on which requests_session are sent.
    """
    global HOST
    HOST = new_host


def set_tokens(new_tokens):
    """
    Store authentication token to reuse them in all requests_session.
    """
    global tokens
    tokens = new_tokens


def make_auth_header():
    global tokens
    if "access_token" in tokens:
        return {"Authorization": "Bearer %s" % tokens["access_token"]}
    else:
        return {}


def url_path_join(*items):
    """
    Make it easier to build url path by joining every arguments with a '/'
    character.
    """
    return "/".join([item.lstrip('/').rstrip('/') for item in items])


def get_full_url(path):
    """
    Join configured host url with given path.
    """
    return url_path_join(get_host(), path)


def get(path):
    """
    Run a get request toward given path for configured host.
    """
    response = requests_session.get(
        get_full_url(path),
        headers=make_auth_header()
    )
    check_status(response.status_code, path)
    return response.json()


def post(path, data):
    """
    Run a post request toward given path for configured host.
    """
    response = requests_session.post(
        get_full_url(path),
        json=data,
        headers=make_auth_header()
    )
    check_status(response.status_code, path)
    return response.json()


def put(path, data):
    """
    Run a put request toward given path for configured host.
    """
    response = requests_session.put(
        get_full_url(path),
        json=data,
        headers=make_auth_header()
    )
    check_status(response.status_code, path)
    return response.json()


def delete(path):
    """
    Run a get request toward given path for configured host.
    """
    response = requests_session.delete(
        get_full_url(path),
        headers=make_auth_header()
    )
    check_status(response.status_code, path)
    return response.text


def check_status(status_code, path):
    """
    Raise an exception related to status code, if the status code does not match
    a success code.
    """
    if (status_code == 404):
        raise RouteNotFoundException(path)
    elif (status_code == 403):
        raise NotAllowedException(path)
    elif (status_code in [401, 422]):
        raise NotAuthenticatedException(path)
    elif (status_code in [500, 502]):
        raise ServerErrorException(path)
    return status_code


def fetch_all(model):
    """
    Get all entries for a given model.
    """
    return get(url_path_join('data', model))


def fetch_one(model, id):
    """
    Get one entry for given model.
    """
    return get(url_path_join('data', model, id))


def create(model, data):
    """
    Get a new entry for given model.
    """
    return post(url_path_join('data', model), data)


def get_api_version():
    """
    Get current version of the API.
    """
    return get('')['version']


def upload(path, file_path):
    """
    Upload file located at *file_path* to given url *path*.
    """
    url = get_full_url(path)
    files = {"file": open(file_path, "rb")}
    return requests_session.post(url, files=files).json()
