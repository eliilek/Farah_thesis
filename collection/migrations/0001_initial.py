# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-06 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConjugateStimulusResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_number', models.PositiveSmallIntegerField()),
                ('play_time', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='ConjugateStimulusResultsBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('completed', models.BooleanField(default=False)),
                ('session_number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PairedStimulusResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_selected', models.NullBooleanField(choices=[(False, 'Left'), (True, 'Right')])),
            ],
        ),
        migrations.CreateModel(
            name='PairedStimulusResultsBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(editable=False)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('video_id', models.CharField(max_length=50)),
                ('start_time', models.PositiveSmallIntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Stimuli',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='stimulus',
            name='subjects',
            field=models.ManyToManyField(to='collection.Subject'),
        ),
        migrations.AddField(
            model_name='pairedstimulusresultsblock',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.Subject'),
        ),
        migrations.AddField(
            model_name='pairedstimulusresult',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.PairedStimulusResultsBlock'),
        ),
        migrations.AddField(
            model_name='pairedstimulusresult',
            name='video_left',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LeftStimResult', to='collection.Stimulus'),
        ),
        migrations.AddField(
            model_name='pairedstimulusresult',
            name='video_right',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RightStimResult', to='collection.Stimulus'),
        ),
        migrations.AddField(
            model_name='conjugatestimulusresultsblock',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.Subject'),
        ),
        migrations.AddField(
            model_name='conjugatestimulusresult',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.ConjugateStimulusResultsBlock'),
        ),
        migrations.AddField(
            model_name='conjugatestimulusresult',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.Stimulus'),
        ),
    ]
