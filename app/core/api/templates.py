from app import app, auth
from flask import Blueprint, g, jsonify, abort, url_for, request
from sqlalchemy import inspect
import datetime


class APITemplate(object):
    def __init__(self):
        self.model = ''
        self.required = []
        self.access = []

    def required_fields(self, response):
        for item in self.model.__required__:
            if item in response:
                if item is None:
                    abort(400)

    def check_unique(self, kwargs, model=None):
        if model:
            self.model = model
        if self.model.query.filter_by(
                **kwargs
                ).first() is not None:
            abort(400)

    def check_privilege(self):
        if g.user.role not in self.access:
            abort(401)

    def public(self):
        if g.user.role == 'limited':
            self.model.__public__ = self.model.__limited__
        if g.user.role == 'member':
            self.model.__public__ = self.model.__member__
        if g.user.role == 'admin':
            self.model.__public__ = self.model.__admin__

    def get(self, id):
        item = self.model.get(id)
        self.public()
        if not item:
            abort(400)
        name = self.model.__name__.lower()
        return jsonify({name: item.get_public()}), 200

    def get_list(self):
        item_list = []
        items = self.model.query.all()
        self.public()
        for item in items:
            item_list.append(item.get_public())
        if not item:
            abort(400)
        name = self.model.__name__.lower() + 's'
        return jsonify({name: item_list}), 200

    def update(self, id, url, data):
        item = self.model.create(**data)
        return (jsonify(item.get_public()), 201,
                {'Location': url_for(url, id=item.id, _external=True)})

        # To REVIST - ability to create datasets that contain multiple
        # models to insert to.
    def create(self, data_set, url):
        for db, data in data_set:
            print db
            create = db.create(**data)
        id = create['id']
        item = self.model.get(id)
        return (jsonify(item.get_public()), 201,
                {'Location': url_for(url, id=item.id, _external=True)})
