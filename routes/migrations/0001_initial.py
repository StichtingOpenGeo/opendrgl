# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table(u'routes_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'routes', ['Route'])

        # Adding model 'Trip'
        db.create_table(u'routes_trip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['routes.Route'])),
        ))
        db.send_create_signal(u'routes', ['Trip'])


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table(u'routes_route')

        # Deleting model 'Trip'
        db.delete_table(u'routes_trip')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'routes.route': {
            'Meta': {'object_name': 'Route'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'routes.trip': {
            'Meta': {'object_name': 'Trip'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['routes.Route']"})
        }
    }

    complete_apps = ['routes']