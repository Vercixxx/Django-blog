# Generated by Django 4.2.3 on 2023-07-11 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0002_alter_post_id_alter_post_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.TextField(default='User')),
                ('likes', models.IntegerField()),
                ('content', models.TextField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='posts_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comment')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'db_table': 'posts_comments',
            },
        ),
    ]
