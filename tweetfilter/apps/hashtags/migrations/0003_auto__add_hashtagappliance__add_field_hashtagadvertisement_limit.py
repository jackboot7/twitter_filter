# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HashtagAppliance'
        db.create_table(u'hashtags_hashtagappliance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashtag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hashtags.HashtagAdvertisement'])),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'hashtags', ['HashtagAppliance'])

        # Adding field 'HashtagAdvertisement.limit'
        db.add_column(u'hashtags_hashtagadvertisement', 'limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'HashtagAppliance'
        db.delete_table(u'hashtags_hashtagappliance')

        # Deleting field 'HashtagAdvertisement.limit'
        db.delete_column(u'hashtags_hashtagadvertisement', 'limit')


    models = {
        u'accounts.channel': {
            'Meta': {'object_name': 'Channel'},
            'allow_messages': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'blacklist_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filters_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['accounts.ItemGroup']", 'symmetrical': 'False'}),
            'hashtags_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'prevent_update_limit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'replacements_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retweet_dm': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retweet_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retweets_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scheduleblocks_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scheduling_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'streaming_task': ('picklefield.fields.PickledObjectField', [], {}),
            'triggers_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'accounts.itemgroup': {
            'Meta': {'object_name': 'ItemGroup'},
            'channel_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            u'scheduleblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['control.ScheduleBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'hashtags.hashtagappliance': {
            'Meta': {'object_name': 'HashtagAppliance'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hashtag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hashtags.HashtagAdvertisement']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['hashtags']