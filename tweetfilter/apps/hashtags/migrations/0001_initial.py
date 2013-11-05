# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HashtagAdvertisement'
        db.create_table(u'hashtags_hashtagadvertisement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['control.ScheduleBlock'], null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hashtags', ['HashtagAdvertisement'])


    def backwards(self, orm):
        # Deleting model 'HashtagAdvertisement'
        db.delete_table(u'hashtags_hashtagadvertisement')


    models = {
        u'control.scheduleblock': {
            'Meta': {'object_name': 'ScheduleBlock'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'hashtags.hashtagadvertisement': {
            'Meta': {'object_name': 'HashtagAdvertisement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['control.ScheduleBlock']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['hashtags']