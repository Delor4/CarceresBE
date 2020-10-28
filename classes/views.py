import re
from datetime import timezone
from email.utils import format_datetime

from flask import jsonify, request
from flask_restful import abort, marshal
from sqlalchemy import asc, desc

from classes.config import config
from db import session


def make_time_headers(obj):
    d = obj.updated_on
    return {
        "Last-Modified": format_datetime(d.replace(tzinfo=timezone.utc), usegmt=True)
    }


def list_view(model_class, resource_fields, resource_url):
    sort_params, sort_arg = _extract_sort_params()
    return jsonify(get_paginated_list(
        session.query(model_class).order_by(*sort_params),
        resource_fields,
        resource_url,
        sort_arg=sort_arg,
        start=int(request.args.get('start', 1)),
        limit=int(request.args.get('limit', config['DEFAULT_PAGE_LIMIT'])),
    ))


def _get_sort_param(sort_param):
    m = re.search('^(desc|asc)\((\S+)\)$', sort_param)
    return (desc if m.group(1) == 'desc' else asc)(m.group(2)) if m else sort_param


def _extract_sort_params():
    params = [a.strip() for a in request.args.get('sort_by', '').split(',')]
    params = list(filter(lambda a: a.strip() != '', params))
    ret = [_get_sort_param(sort_param) for sort_param in params]

    return ret, 'sort_by=' + ','.join(params) if params else ''


def _add_arg(uri, args):
    return uri + '&' + args if args else uri


def get_paginated_list(obj_list, resource_fields, resource_url, sort_arg, start, limit):
    # Pagination based on:
    # https://aviaryan.com/blog/gsoc/paginated-apis-flask

    # check if page exists
    count = obj_list.count()

    # make response
    obj = {'start': start, 'limit': limit, 'count': count, 'previous': '', 'next': ''}
    # check bounds
    if count == 0:
        obj['results'] = []
        return obj
    if start < 1 or count < start:
        abort(404, message=f"Pagination start outside allowed values. Expected: 1 - {count}. Provided: {start}")
    if limit < 1:
        abort(404, message=f"Pagination limit outside allowed values. Expected more than 0. Provided: {limit}")

    # make URLs
    # make previous url
    if start != 1:
        start_copy = max(1, start - limit)
        limit_copy = min(limit, start - 1)
        obj['previous'] = _add_arg(resource_url + '?start=%d&limit=%d' % (start_copy, limit_copy), sort_arg)
    # make next url
    if start + limit <= count:
        start_copy = start + limit
        obj['next'] = _add_arg(resource_url + '?start=%d&limit=%d' % (start_copy, limit), sort_arg)

    # finally extract result according to bounds
    results = obj_list.limit(limit).offset(start - 1).all()
    obj['results'] = marshal(results, resource_fields)

    return obj
