# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    name = models.CharField(unique=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Comments(models.Model):
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Enrollments(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'enrollments'


class Events(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, db_column='category', blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    current_participants = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'events'


class Users(models.Model):
    username = models.TextField()
    email = models.TextField(unique=True)
    password_hash = models.TextField()
    role = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'users'
