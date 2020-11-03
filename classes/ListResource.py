import re

from flask import jsonify, request
from flask import url_for
from flask_restful import abort, marshal
from sqlalchemy import asc, desc

from classes.ResourceBase import ResourceBase
from classes.auth import nocache
from classes.config import config
from db import session


class ListResource(ResourceBase):
    __abstract__ = True

    def __init__(self):
        super(ListResource, self).__init__()
        self.model_class = None
        self.model_name = None
        self.marshal_fields = None

    def process_get_req(self, models=None):
        """
        Return list of models. Apply pagination and sorting args from request query.
        """
        return self.list_view(models)

    @nocache
    def finalize_post_req(self, model):
        """
        Save model in database. Return to client with appropriate status code and headers.
        """
        session.add(model)
        self.try_session_commit()
        return model, 201, self.make_response_headers(location=url_for(self.model_name, id=model.id, _external=True))

    def list_view(self, models):
        sort_params, sort_arg = self._extract_sort_params()
        return jsonify(self.get_paginated_list(
            models,
            sort_params,
            sort_arg=sort_arg,
            start=int(request.args.get('start', 1)),
            limit=int(request.args.get('limit', config['DEFAULT_PAGE_LIMIT'])),
        ))

    def get_paginated_list(self, models, sort_params, sort_arg, start, limit):
        # Pagination based on:
        # https://aviaryan.com/blog/gsoc/paginated-apis-flask

        if models is not None:
            obj_list = models
        else:
            obj_list = session.query(self.model_class).order_by(*sort_params)

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
        resource_url = url_for(self.endpoint, _external=True)
        # make previous url
        if start != 1:
            start_copy = max(1, start - limit)
            limit_copy = min(limit, start - 1)
            obj['previous'] = self._add_arg(resource_url + '?start=%d&limit=%d' % (start_copy, limit_copy), sort_arg)
        # make next url
        if start + limit <= count:
            start_copy = start + limit
            obj['next'] = self._add_arg(resource_url + '?start=%d&limit=%d' % (start_copy, limit), sort_arg)

        # finally extract result according to bounds
        results = obj_list.limit(limit).offset(start - 1).all()
        obj['results'] = marshal(results, self.marshal_fields)

        return obj

    @staticmethod
    def _get_sort_param(sort_param):
        m = re.search("^(desc|asc)\((\S+)\)$", sort_param)
        return (desc if m.group(1) == 'desc' else asc)(m.group(2)) if m else sort_param

    def _extract_sort_params(self):
        params = [a.strip() for a in request.args.get('sort_by', '').split(',')]
        params = list(filter(lambda a: a.strip() != '', params))
        ret = [self._get_sort_param(sort_param) for sort_param in params]

        return ret, 'sort_by=' + ','.join(params) if params else ''

    @staticmethod
    def _add_arg(uri, args):
        return uri + '&' + args if args else uri
