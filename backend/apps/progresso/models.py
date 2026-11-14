from django.db import models
from django.db.models import UniqueConstraint

class Progresso(models.Model):
    id_progresso = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE)
    id_item_matriz = models.ForeignKey('matrizes.MatrizDisciplina', on_delete=models.PROTECT)
    situacao = models.CharField(max_length=50)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_aluno', 'id_item_matriz'], name='uq_progresso')]
