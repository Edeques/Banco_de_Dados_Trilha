from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # E-mail normalizado único
    password = models.CharField(max_length=255, db_column='senha_hash')
    id_curso = models.ForeignKey('cursos.Curso', on_delete=models.PROTECT, db_column='id_curso')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'


class Aluno(models.Model):
    id_usuario = models.OneToOneField(
        'usuarios.Usuario',
        primary_key=True,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    id_matriz_ativa = models.ForeignKey(
        'matrizes.Matriz',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_matriz_ativa'
    )

    class Meta:
        db_table = 'aluno'


class Coordenador(models.Model):
    id_usuario = models.OneToOneField(
        'usuarios.Usuario',
        primary_key=True,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    class Meta:
        db_table = 'coordenador'