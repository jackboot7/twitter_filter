# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlockedUser'
        db.create_table(u'filtering_blockeduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('block_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('block_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
        ))
        db.send_create_signal(u'filtering', ['BlockedUser'])

        # Adding model 'AllowedUser'
        db.create_table(u'filtering_alloweduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
        ))
        db.send_create_signal(u'filtering', ['AllowedUser'])

        # Adding model 'ChannelScheduleBlock'
        db.create_table(u'filtering_channelscheduleblock', (
            (u'scheduleblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['control.ScheduleBlock'], unique=True, primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
            ('allow_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_dm', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'filtering', ['ChannelScheduleBlock'])

        # Adding model 'Keyword'
        db.create_table(u'filtering_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'filtering', ['Keyword'])

        # Adding model 'Trigger'
        db.create_table(u'filtering_trigger', (
            (u'keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['filtering.Keyword'], unique=True, primary_key=True)),
            ('action', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
            ('enabled_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enabled_dm', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'filtering', ['Trigger'])

        # Adding model 'Filter'
        db.create_table(u'filtering_filter', (
            (u'keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['filtering.Keyword'], unique=True, primary_key=True)),
            ('action', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
            ('enabled_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enabled_dm', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'filtering', ['Filter'])

        # Adding model 'Replacement'
        db.create_table(u'filtering_replacement', (
            (u'keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['filtering.Keyword'], unique=True, primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Channel'])),
            ('replace_with', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'filtering', ['Replacement'])


    def backwards(self, orm):
        # Deleting model 'BlockedUser'
        db.delete_table(u'filtering_blockeduser')

        # Deleting model 'AllowedUser'
        db.delete_table(u'filtering_alloweduser')

        # Deleting model 'ChannelScheduleBlock'
        db.delete_table(u'filtering_channelscheduleblock')

        # Deleting model 'Keyword'
        db.delete_table(u'filtering_keyword')

        # Deleting model 'Trigger'
        db.delete_table(u'filtering_trigger')

        # Deleting model 'Filter'
        db.delete_table(u'filtering_filter')

        # Deleting model 'Replacement'
        db.delete_table(u'filtering_replacement')


    models = {
        u'accounts.channel': {
            'Meta': {'object_name': 'Channel'},
            'allow_messages': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'streaming_task': ('picklefield.fields.PickledObjectField', [], {}),
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
        u'filtering.alloweduser': {
            'Meta': {'object_name': 'AllowedUser'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'filtering.blockeduser': {
            'Meta': {'object_name': 'BlockedUser'},
            'block_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'block_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'filtering.channelscheduleblock': {
            'Meta': {'object_name': 'ChannelScheduleBlock', '_ormbases': [u'control.ScheduleBlock']},
            'allow_dm': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            u'scheduleblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['control.ScheduleBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'filtering.filter': {
            'Meta': {'object_name': 'Filter', '_ormbases': [u'filtering.Keyword']},
            'action': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            'enabled_dm': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['filtering.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'filtering.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'filtering.replacement': {
            'Meta': {'object_name': 'Replacement', '_ormbases': [u'filtering.Keyword']},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            u'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['filtering.Keyword']", 'unique': 'True', 'primary_key': 'True'}),
            'replace_with': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'filtering.trigger': {
            'Meta': {'object_name': 'Trigger', '_ormbases': [u'filtering.Keyword']},
            'action': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Channel']"}),
            'enabled_dm': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['filtering.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['filtering']