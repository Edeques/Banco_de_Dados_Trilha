from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True) # E-mail normalizado único
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        db_table = 'usuario'

class Aluno(models.Model):
    id_usuario = models.OneToOneField('usuarios.Usuario', primary_key=True, on_delete=models.CASCADE)
    id_matriz_ativa = models.ForeignKey('matrizes.Matriz', on_delete=models.SET_NULL, null=True, blank=True)

class Coordenador(models.Model):
    id_usuario = models.OneToOneField('usuarios.Usuario', primary_key=True, on_delete=models.CASCADE)