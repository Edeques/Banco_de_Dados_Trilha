# Modelos Django - Base persistente do Trilha (15 tabelas do domínio)
# ATENÇÃO: Conforme o documento, distribua estas classes nos respectivos apps:
# apps/usuarios/models.py, apps/cursos/models.py, apps/matrizes/models.py, etc.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, F, UniqueConstraint, CheckConstraint

# --- CURSOS ---
class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)

# --- USUÁRIOS ---
class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True) # E-mail normalizado único
    id_curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        db_table = 'usuario'

class Aluno(models.Model):
    id_usuario = models.OneToOneField(Usuario, primary_key=True, on_delete=models.CASCADE)
    id_matriz_ativa = models.ForeignKey('Matriz', on_delete=models.SET_NULL, null=True, blank=True)

class Coordenador(models.Model):
    id_usuario = models.OneToOneField(Usuario, primary_key=True, on_delete=models.CASCADE)

# --- MATRIZES & DISCIPLINAS ---
class Matriz(models.Model):
    STATUS_CHOICES = [('RASCUNHO', 'Rascunho'), ('VIGENTE', 'Vigente'), ('ARQUIVADA', 'Arquivada')]
    id_matriz = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
    qtd_optativas_necessarias = models.IntegerField(default=0)
    versao = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_curso', 'titulo', 'ano', 'versao'], name='uq_matriz'),
            CheckConstraint(check=Q(ano__gt=0), name='chk_matriz_ano'),
            CheckConstraint(check=Q(versao__gt=0), name='chk_matriz_versao'),
            CheckConstraint(check=Q(qtd_optativas_necessarias__gte=0), name='chk_matriz_optativas')
        ]

class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    ementa = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_curso', 'codigo'], name='uq_disciplina_curso')]

class MatrizDisciplina(models.Model):
    id_item_matriz = models.AutoField(primary_key=True)
    id_matriz = models.ForeignKey(Matriz, on_delete=models.PROTECT)
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    semestre = models.IntegerField()
    creditos = models.IntegerField()
    tipo = models.CharField(max_length=50)
    horas = models.IntegerField()
    min_creditos = models.IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_matriz', 'id_disciplina'], name='uq_matriz_disciplina'),
            CheckConstraint(check=Q(semestre__gt=0), name='chk_md_semestre'),
            CheckConstraint(check=Q(creditos__gte=0), name='chk_md_creditos'),
            CheckConstraint(check=Q(horas__gte=0), name='chk_md_horas'),
            CheckConstraint(check=Q(min_creditos__gte=0), name='chk_md_min_creditos')
        ]

class PreRequisito(models.Model):
    id_item_dependente = models.ForeignKey(MatrizDisciplina, related_name='dependentes', on_delete=models.CASCADE)
    id_item_requisito = models.ForeignKey(MatrizDisciplina, related_name='requisitos', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_item_dependente', 'id_item_requisito'),)
        constraints = [
            CheckConstraint(check=~Q(id_item_dependente=F('id_item_requisito')), name='chk_no_self_reference')
        ]

# --- OFERTAS ---
class Oferta(models.Model):
    STATUS_CHOICES = [('RASCUNHO', 'Rascunho'), ('PUBLICADA', 'Publicada'), ('ENCERRADA', 'Encerrada'), ('CANCELADA', 'Cancelada')]
    id_oferta = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    id_criador = models.ForeignKey(Coordenador, on_delete=models.PROTECT)
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
    id_oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_oferta', 'id_disciplina'], name='uq_item_oferta')]

class Encontro(models.Model):
    id_encontro = models.AutoField(primary_key=True)
    id_item_oferta = models.ForeignKey(ItemOferta, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(dia_semana__gte=1) & Q(dia_semana__lte=7), name='chk_dia_semana'),
            CheckConstraint(check=Q(horario_fim__gt=F('horario_inicio')), name='chk_horario_fim')
        ]

# --- PROGRESSO & PLANEJAMENTO ---
class Progresso(models.Model):
    id_progresso = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    id_item_matriz = models.ForeignKey(MatrizDisciplina, on_delete=models.PROTECT)
    situacao = models.CharField(max_length=50)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_aluno', 'id_item_matriz'], name='uq_progresso')]

class Planejamento(models.Model):
    id_planejamento = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    id_matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

class SemestrePlanejamento(models.Model):
    id_semestre_planejamento = models.AutoField(primary_key=True)
    id_planejamento = models.ForeignKey(Planejamento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    ordem = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_planejamento', 'ordem'], name='uq_semestre_ordem'),
            CheckConstraint(check=Q(ordem__gt=0), name='chk_sem_ordem')
        ]

class ItemPlanejamento(models.Model):
    id_item_planejamento = models.AutoField(primary_key=True)
    id_semestre_planejamento = models.ForeignKey(SemestrePlanejamento, on_delete=models.CASCADE)
    id_item_matriz = models.ForeignKey(MatrizDisciplina, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['id_semestre_planejamento', 'id_item_matriz'], name='uq_item_plan_semestre')]
