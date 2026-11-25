from django.db import models
from django.db.models import UniqueConstraint


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True, db_column='id_disciplina')
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT, db_column='id_curso')
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    ementa = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'disciplina'
        constraints = [
            UniqueConstraint(fields=['id_curso', 'codigo'], name='uq_disciplina_curso')
        ]