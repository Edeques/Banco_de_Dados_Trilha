import os
import django

# Configurar o ambiente do Django para permitir o uso do ORM fora do servidor
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cursos.models import Curso
from apps.usuarios.models import Usuario, Coordenador, Aluno

def popular_banco():
    print("A iniciar a injeção de dados de teste...")
    
    # 1. Criar o Curso Base
    curso_teste, criado = Curso.objects.get_or_create(
        codigo="CC01", 
        defaults={"nome": "Ciência da Computação"}
    )
    
    # 2. Criar a conta do Coordenador
    if not Usuario.objects.filter(email="coordenador@trilha.edu").exists():
        user_coord = Usuario(nome="Carlos Silva", email="coordenador@trilha.edu", id_curso=curso_teste)
        user_coord.set_password("senha123") # Encripta a palavra-passe
        user_coord.save()
        Coordenador.objects.create(id_usuario=user_coord)
        print("- Conta de Coordenador criada com sucesso.")
        
    # 3. Criar a conta do Aluno
    if not Usuario.objects.filter(email="aluno@trilha.edu").exists():
        user_aluno = Usuario(nome="Ana Rodrigues", email="aluno@trilha.edu", id_curso=curso_teste)
        user_aluno.set_password("senha123") # Encripta a palavra-passe
        user_aluno.save()
        Aluno.objects.create(id_usuario=user_aluno)
        print("- Conta de Aluno criada com sucesso.")

    print("Processo concluído! Os seus colegas já podem fazer login.")

if __name__ == '__main__':
    popular_banco()