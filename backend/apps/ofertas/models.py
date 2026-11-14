from django.db import models
from django.db.models import Q, F, UniqueConstraint, CheckConstraint

class Oferta(models.Model):
    STATUS_CHOICES = [('RASCUNHO', 'Rascunho'), ('PUBLICADA', 'Publicada'), ('ENCERRADA', 'Encerrada'), ('CANCELADA', 'Cancelada')]
    id_oferta = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT)
    id_criador = models.ForeignKey('usuarios.Coordenador', on_delete=models.PROTECT)
    semestre_letivo = models.CharField(max_length=50)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_encerramento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_curso'], condition=Q(status='PUBLICADA'), name='uq_oferta_publicada_curso')
        ]

class ItemOferta(models.Model):
    id_item_oferta = models.AutoField(primary_key=True)
    id_oferta = models.ForeignKey('ofertas.Oferta', on_delete=models.CASCADE)
    id_disciplina = models.ForeignKey('disciplinas.Disciplina', on_delete=models.PROTECT)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_oferta', 'id_disciplina'], name='uq_item_oferta')]

class Encontro(models.Model):
    id_encontro = models.AutoField(primary_key=True)
    id_item_oferta = models.ForeignKey('ofertas.ItemOferta', on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(dia_semana__gte=1) & Q(dia_semana__lte=7), name='chk_dia_semana'),
            CheckConstraint(condition=Q(horario_fim__gt=F('horario_inicio')), name='chk_horario_fim')
        ]