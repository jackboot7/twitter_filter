# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tweet', fields ['tweet_id']
        db.delete_unique(u'twitter_tweet', ['tweet_id'])


    def backwards(self, orm):
        # Adding unique constraint on 'Tweet', fields ['tweet_id']
        db.create_unique(u'twitter_tweet', ['tweet_id'])


    models = {
        u'twitter.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hashtags': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_urls': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'mention_to': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'retweeted_text': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '16'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['twitter']