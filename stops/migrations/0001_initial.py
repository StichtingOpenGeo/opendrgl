# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stop'
        db.create_table(u'stops_stop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('stop_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'stops', ['Stop'])

        # Adding unique constraint on 'Stop', fields ['project', 'stop_id']
        db.create_unique(u'stops_stop', ['project_id', 'stop_id'])

        # Adding model 'Quay'
        db.create_table(u'stops_quay', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('quay_id', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'stops', ['Quay'])

        # Adding unique constraint on 'Quay', fields ['project', 'quay_id']
        db.create_unique(u'stops_quay', ['project_id', 'quay_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Quay', fields ['project', 'quay_id']
        db.delete_unique(u'stops_quay', ['project_id', 'quay_id'])

        # Removing unique constraint on 'Stop', fields ['project', 'stop_id']
        db.delete_unique(u'stops_stop', ['project_id', 'stop_id'])

        # Deleting model 'Stop'
        db.delete_table(u'stops_stop')

        # Deleting model 'Quay'
        db.delete_table(u'stops_quay')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stops.quay': {
            'Meta': {'unique_together': "(('project', 'quay_id'),)", 'object_name': 'Quay'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'quay_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'stops.stop': {
            'Meta': {'unique_together': "(('project', 'stop_id'),)", 'object_name': 'Stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['stops']