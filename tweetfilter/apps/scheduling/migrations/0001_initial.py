# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScheduledTweet'
        db.create_table(u'scheduling_scheduledtweet', (
            (u'schedule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['control.Schedule'], unique=True, primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.ItemGroup'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('periodic_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djcelery.PeriodicTask'], null=True, blank=True)),
        ))
        db.send_create_signal(u'scheduling', ['ScheduledTweet'])


    def backwards(self, orm):
        # Deleting model 'ScheduledTweet'
        db.delete_table(u'scheduling_scheduledtweet')


    models = {
        u'accounts.itemgroup': {
            'Meta': {'object_name': 'ItemGroup'},
            'channel_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'control.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'djcelery.crontabschedule': {
            'Meta': {'object_name': 'CrontabSchedule'},
            'day_of_month': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            'day_of_week': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            'month_of_year': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'})
        },
        u'djcelery.intervalschedule': {
            'Meta': {'object_name': 'IntervalSchedule'},
            'every': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        u'djcelery.periodictask': {
            'Meta': {'object_name': 'PeriodicTask'},
            'args': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'crontab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.CrontabSchedule']", 'null': 'True', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exchange': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.IntervalSchedule']", 'null': 'True', 'blank': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'last_run_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'queue': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'routing_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_run_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'scheduling.scheduledtweet': {
            'Meta': {'object_name': 'ScheduledTweet', '_ormbases': [u'control.Schedule']},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.ItemGroup']", 'null': 'True', 'blank': 'True'}),
            'periodic_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.PeriodicTask']", 'null': 'True', 'blank': 'True'}),
            u'schedule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['control.Schedule']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['scheduling']