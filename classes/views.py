from flask import jsonify, request
from flask_restful import abort, marshal

from db import session


# Pagination based on:
# https://aviaryan.com/blog/gsoc/paginated-apis-flask


def list_view(model_class, resource_fields, resource_url):
    return jsonify(get_paginated_list(
        model_class,
        resource_fields,
        resource_url,
        start=int(request.args.get('start', 1)),
        limit=int(request.args.get('limit', 20))
    ))


def get_paginated_list(model_class, resource_fields, resource_url, start, limit):
    # check if page exists
    results = session.query(model_class).all()
    count = len(results)
    # make response
    obj = {'start': start, 'limit': limit, 'count': count}
    # check bounds
    if count == 0:
        obj['results'] = []
        return obj
    if start < 1 or count < start:
        abort(404, message=f"Pagination start outside allowed values. Expected: 1 - {count}. Provided: {start}")
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = resource_url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = resource_url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = marshal(results[(start - 1):(start - 1 + limit)], resource_fields)

    return obj
