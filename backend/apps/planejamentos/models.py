from django.db import models
from django.db.models import Q, UniqueConstraint, CheckConstraint


class Planejamento(models.Model):
    id_planejamento = models.AutoField(primary_key=True, db_column='id_planejamento')
    id_aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE, db_column='id_aluno')
    id_matriz = models.ForeignKey('matrizes.Matriz', on_delete=models.CASCADE, db_column='id_matriz')
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'planejamento'


class SemestrePlanejamento(models.Model):
    id_semestre_planejamento = models.AutoField(primary_key=True, db_column='id_semestre_planejamento')
    id_planejamento = models.ForeignKey('planejamentos.Planejamento', on_delete=models.CASCADE, db_column='id_planejamento')
    nome = models.CharField(max_length=255)
    ordem = models.IntegerField()

    class Meta:
        db_table = 'semestre_planejamento'
        constraints = [
            UniqueConstraint(fields=['id_planejamento', 'ordem'], name='uq_semestre_ordem'),
            CheckConstraint(condition=Q(ordem__gt=0), name='chk_sem_ordem'),
        ]


class ItemPlanejamento(models.Model):
    id_item_planejamento = models.AutoField(primary_key=True, db_column='id_item_planejamento')
    id_semestre_planejamento = models.ForeignKey('planejamentos.SemestrePlanejamento', on_delete=models.CASCADE, db_column='id_semestre_planejamento')
    id_item_matriz = models.ForeignKey('matrizes.MatrizDisciplina', on_delete=models.CASCADE, db_column='id_item_matriz')

    class Meta:
        db_table = 'item_planejamento'
        constraints = [
            UniqueConstraint(fields=['id_semestre_planejamento', 'id_item_matriz'], name='uq_item_plan_semestre')
        ]