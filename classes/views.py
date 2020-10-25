from flask import jsonify, request
from flask_restful import abort, marshal

from classes.config import config
from db import session


# Pagination based on:
# https://aviaryan.com/blog/gsoc/paginated-apis-flask


def list_view(model_class, resource_fields, resource_url):
    return jsonify(get_paginated_list(
        model_class,
        resource_fields,
        resource_url,
        start=int(request.args.get('start', 1)),
        limit=int(request.args.get('limit', config['DEFAULT_PAGE_LIMIT']))
    ))


def get_paginated_list(model_class, resource_fields, resource_url, start, limit):
    # check if page exists
    count = session.query(model_class).count()
    # count = session.query(func.count(model_class.id)).scalar()

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
        obj['previous'] = resource_url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit <= count:
        start_copy = start + limit
        obj['next'] = resource_url + '?start=%d&limit=%d' % (start_copy, limit)

    # finally extract result according to bounds
    results = session.query(model_class).limit(limit).offset(start - 1).all()
    obj['results'] = marshal(results, resource_fields)

    return obj
