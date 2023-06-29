# Generated by Django 4.2.1 on 2023-05-10 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('img1', models.ImageField(upload_to='image/%Y')),
                ('img2', models.ImageField(upload_to='image/%Y')),
                ('img3', models.ImageField(upload_to='image/%Y')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ContentPage.brand')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ContentPage.image')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ContentPage.products')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ContentPage.size')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='sizes',
            field=models.ManyToManyField(through='ContentPage.ProductSize', to='ContentPage.size'),
        ),
    ]