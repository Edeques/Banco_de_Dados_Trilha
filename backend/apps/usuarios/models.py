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

# CLASSE 1: Usuario
class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, db_column='senha_hash')
    last_login = None

    # Mantenha outros campos que existam aqui (ex: tipo, ativo, etc.)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'


# CLASSE 2: Aluno
class Aluno(models.Model):
    id_usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        db_column='id_usuario'
    )
    id_curso = models.ForeignKey(
        'cursos.Curso', 
        on_delete=models.PROTECT, 
        db_column='id_curso'
    )
    # Mantenha outros campos que existam aqui (ex: matricula, semestre_atual, etc.)

    class Meta:
        db_table = 'aluno'


# CLASSE 3: Coordenador
class Coordenador(models.Model):
    id_usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        db_column='id_usuario'
    )
    id_curso = models.ForeignKey(
        'cursos.Curso', 
        on_delete=models.PROTECT, 
        db_column='id_curso'
    )
    # Mantenha outros campos que existam aqui (ex: siape, etc.)

    class Meta:
        db_table = 'coordenador'