from django.db import models
from django.db.models import UniqueConstraint

class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT)
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    ementa = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_curso', 'codigo'], name='uq_disciplina_curso')]