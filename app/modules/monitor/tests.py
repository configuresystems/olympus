from app import db
from app.testing import BaseTestCase
from app.core.auth.tests import AuthTestTemplates
from .models import Monitor, MonitorResponse, Device, Region, State
from flask import url_for
import json
import base64
import datetime

class MonitorTestTemplates(BaseTestCase):
    pass


class MonitorTests(MonitorTestTemplates, AuthTestTemplates):

    def setUp(self):
        db.create_all()
        device = Device.create(
                name='ping',
                created=datetime.datetime.utcnow()
                )
        device = Device.get(device.id)
        self.assertEqual('ping', device.name)
        state = State.create(
                name='online',
                created=datetime.datetime.utcnow()
                )
        state = State.get(state.id)
        self.assertEqual('online', state.name)
        region = Region.create(
                name='east',
                ip='150.150.150.150',
                zone='a',
                created=datetime.datetime.utcnow()
                )
        region = Region.get(region.id)
        self.assertEqual('east', region.name)
        self.assertEqual('150.150.150.150', region.ip)
        self.assertEqual('a', region.zone)
        monitor = Monitor.create(
                name='acme',
                ip='10.10.10.10',
                alert=1,
                created=datetime.datetime.utcnow()
                )
        monitor = Monitor.get(monitor.id)
        self.assertEqual('acme', monitor.name)
        self.assertEqual('10.10.10.10', monitor.ip)
        self.assertEqual(1, monitor.alert)

        monitor_response = MonitorResponse.create(
                device_name=device.name,
                state_name=state.name,
                region_name=region.name,
                count=1,
                monitor_id=monitor.id,
                created=datetime.datetime.utcnow(),
                updated=datetime.datetime.utcnow()
                )
        monitor_response = MonitorResponse.get(monitor_response.id)
        self.assertEqual(monitor.id, monitor_response.monitor_id)
        self.assertEqual(device.name, monitor_response.device_name)
        self.assertEqual(state.name, monitor_response.state_name)
        self.assertEqual(region.name, monitor_response.region_name)


    def test_monitor_get(self):
        response = self.client.get(
                url_for('monitoring.get', id=1),
                content_type='application/json'
                )
        print response.data

    def test_monitor_get_list(self):
        response = self.client.get(
                url_for('monitoring.get_list'),
                content_type='application/json'
                )
        print response.data

