# Generated by Django 5.0.6 on 2024-08-10 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0006_category_description_category_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='seo_description',
            field=models.CharField(blank=True, help_text='SEO Описание', max_length=160, null=True, verbose_name='SEO Описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_keywords',
            field=models.CharField(blank=True, help_text='SEO Ключевые слова', max_length=255, null=True, verbose_name='SEO Ключевые слова'),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_title',
            field=models.CharField(blank=True, help_text='SEO Заголовок', max_length=70, null=True, verbose_name='SEO Заголовок'),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_description',
            field=models.CharField(blank=True, help_text='SEO Описание', max_length=160, null=True, verbose_name='SEO Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_keywords',
            field=models.CharField(blank=True, help_text='SEO Ключевые слова', max_length=255, null=True, verbose_name='SEO Ключевые слова'),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.CharField(blank=True, help_text='SEO Заголовок', max_length=70, null=True, verbose_name='SEO Заголовок'),
        ),
    ]
