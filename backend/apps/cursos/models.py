from django.db import models

# CLASSE 4: Curso
class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True, db_column='id_curso')
    # Mantenha os campos de nome, sigla, turno, etc. que já estão no seu arquivo

    class Meta:
        db_table = 'curso'