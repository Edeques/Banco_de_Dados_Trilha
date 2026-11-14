from django.db import models
from django.db.models import Q, F, UniqueConstraint, CheckConstraint

class Matriz(models.Model):
    STATUS_CHOICES = [('RASCUNHO', 'Rascunho'), ('VIGENTE', 'Vigente'), ('ARQUIVADA', 'Arquivada')]
    id_matriz = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT)
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
    qtd_optativas_necessarias = models.IntegerField(default=0)
    versao = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_curso', 'titulo', 'ano', 'versao'], name='uq_matriz'),
            CheckConstraint(condition=Q(ano__gt=0), name='chk_matriz_ano'),
            CheckConstraint(condition=Q(versao__gt=0), name='chk_matriz_versao'),
            CheckConstraint(condition=Q(qtd_optativas_necessarias__gte=0), name='chk_matriz_optativas')
        ]

class MatrizDisciplina(models.Model):
    id_item_matriz = models.AutoField(primary_key=True)
    id_matriz = models.ForeignKey('matrizes.Matriz', on_delete=models.PROTECT)
    id_disciplina = models.ForeignKey('disciplinas.Disciplina', on_delete=models.PROTECT)
    semestre = models.IntegerField()
    creditos = models.IntegerField()
    tipo = models.CharField(max_length=50)
    horas = models.IntegerField()
    min_creditos = models.IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_matriz', 'id_disciplina'], name='uq_matriz_disciplina'),
            CheckConstraint(condition=Q(semestre__gt=0), name='chk_md_semestre'),
            CheckConstraint(condition=Q(creditos__gte=0), name='chk_md_creditos'),
            CheckConstraint(condition=Q(horas__gte=0), name='chk_md_horas'),
            CheckConstraint(condition=Q(min_creditos__gte=0), name='chk_md_min_creditos')
        ]

class PreRequisito(models.Model):
    id_item_dependente = models.ForeignKey('matrizes.MatrizDisciplina', related_name='dependentes', on_delete=models.CASCADE)
    id_item_requisito = models.ForeignKey('matrizes.MatrizDisciplina', related_name='requisitos', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_item_dependente', 'id_item_requisito'),)
        constraints = [
            CheckConstraint(condition=~Q(id_item_dependente=F('id_item_requisito')), name='chk_no_self_reference')
        ]