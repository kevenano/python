# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Main(models.Model):
    id = models.IntegerField(primary_key=True)
    tags = models.TextField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    creator_id = models.IntegerField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    change = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    md5 = models.TextField(blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    is_shown_in_index = models.TextField(blank=True, null=True)
    preview_url = models.TextField(blank=True, null=True)
    preview_width = models.IntegerField(blank=True, null=True)
    preview_height = models.IntegerField(blank=True, null=True)
    actual_preview_width = models.IntegerField(blank=True, null=True)
    actual_preview_height = models.IntegerField(blank=True, null=True)
    sample_url = models.TextField(blank=True, null=True)
    sample_width = models.IntegerField(blank=True, null=True)
    sample_height = models.IntegerField(blank=True, null=True)
    sample_file_size = models.IntegerField(blank=True, null=True)
    jpeg_url = models.TextField(blank=True, null=True)
    jpeg_width = models.IntegerField(blank=True, null=True)
    jpeg_height = models.IntegerField(blank=True, null=True)
    jpeg_file_size = models.IntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    has_children = models.TextField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    is_held = models.TextField(blank=True, null=True)
    frames_pending_string = models.TextField(blank=True, null=True)
    frames_pending = models.TextField(blank=True, null=True)
    frames_string = models.TextField(blank=True, null=True)
    frames = models.TextField(blank=True, null=True)
    flag_detail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main'


class Mark(models.Model):
    id = models.IntegerField(primary_key=True)
    favorite = models.TextField(blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mark'
