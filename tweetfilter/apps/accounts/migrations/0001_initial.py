# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table(u'accounts_channel', (
            ('screen_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, primary_key=True)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('oauth_secret', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('streaming_task', self.gf('picklefield.fields.PickledObjectField')()),
            ('allow_messages', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'accounts', ['Channel'])

        # Adding model 'FilteringConfig'
        db.create_table(u'accounts_filteringconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.Channel'], unique=True)),
            ('retweets_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('retweet_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('retweet_dm', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'accounts', ['FilteringConfig'])

        # Adding model 'SchedulingConfig'
        db.create_table(u'accounts_schedulingconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.Channel'], unique=True)),
            ('scheduling_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'accounts', ['SchedulingConfig'])


    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table(u'accounts_channel')

        # Deleting model 'FilteringConfig'
        db.delete_table(u'accounts_filteringconfig')

        # Deleting model 'SchedulingConfig'
        db.delete_table(u'accounts_schedulingconfig')


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
        u'accounts.filteringconfig': {
            'Meta': {'object_name': 'FilteringConfig'},
            'channel': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.Channel']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retweet_dm': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retweet_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retweets_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'accounts.schedulingconfig': {
            'Meta': {'object_name': 'SchedulingConfig'},
            'channel': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.Channel']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheduling_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        }
    }

    complete_apps = ['accounts']