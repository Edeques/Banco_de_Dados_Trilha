from django.db import models


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True, db_column='id_curso')
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = 'curso'