# Generated by Django 2.0.6 on 2020-11-05 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True)),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
                ('emall', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TArticle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('publish_time', models.DateTimeField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_article',
            },
        ),
        migrations.CreateModel(
            name='TCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_category',
            },
        ),
        migrations.AddField(
            model_name='tarticle',
            name='cate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home_pageapp.TCategory'),
        ),
    ]