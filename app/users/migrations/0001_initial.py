# Generated by Django 5.0.2 on 2024-02-29 14:53

import django.db.models.deletion
import users.models
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('skill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=12, unique=True, verbose_name='phone number')),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('bio', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=users.models.profile_img_path, validators=[users.validators.profile_image_size_validator])),
                ('age', models.PositiveIntegerField(blank=True, null=True, validators=[users.validators.age_validator])),
                ('plan_type', models.CharField(choices=[('FREE', 'Free'), ('BRONZE', 'Bronze'), ('SILVER', 'Silver'), ('GOLD', 'Gold')], default='FREE', max_length=6)),
                ('balance', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('score', models.PositiveIntegerField(default=0)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=2, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('uuid', models.CharField(db_index=True, default=users.models.generate_uuid)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skill_prof', to='users.profile')),
                ('skill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skill_sk', to='skill.skill')),
            ],
            options={
                'unique_together': {('profile_id', 'skill_id')},
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(related_name='skill_profile', through='users.ProfileSkill', to='skill.skill'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='users.profile')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='users.profile')),
            ],
            options={
                'unique_together': {('follower', 'target')},
            },
        ),
    ]
