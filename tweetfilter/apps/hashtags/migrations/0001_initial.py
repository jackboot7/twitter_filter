# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HashtagAdvertisement'
        db.create_table(u'hashtags_hashtagadvertisement', (
            (u'scheduleblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['control.ScheduleBlock'], unique=True, primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.ItemGroup'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'hashtags', ['HashtagAdvertisement'])


    def backwards(self, orm):
        # Deleting model 'HashtagAdvertisement'
        db.delete_table(u'hashtags_hashtagadvertisement')


    models = {
        u'accounts.itemgroup': {
            'Meta': {'object_name': 'ItemGroup'},
            'channel_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
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
            'Meta': {'object_name': 'HashtagAdvertisement', '_ormbases': [u'control.ScheduleBlock']},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.ItemGroup']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            u'scheduleblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['control.ScheduleBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['hashtags']