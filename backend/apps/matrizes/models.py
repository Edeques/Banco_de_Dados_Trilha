from django.db import models

# CLASSE 7: Matriz
class Matriz(models.Model):
    id_matriz = models.AutoField(primary_key=True, db_column='id_matriz')
    id_curso = models.ForeignKey(
        'cursos.Curso', 
        on_delete=models.CASCADE, 
        db_column='id_curso'
    )
    # Mantenha os outros campos (ex: ano, vigente, etc.)

    class Meta:
        db_table = 'matriz'


# CLASSE 8: MatrizDisciplina
class MatrizDisciplina(models.Model):
    id_matriz_disciplina = models.AutoField(primary_key=True, db_column='id_matriz_disciplina')
    id_matriz = models.ForeignKey(
        Matriz, 
        on_delete=models.CASCADE, 
        db_column='id_matriz'
    )
    id_disciplina = models.ForeignKey(
        'disciplinas.Disciplina', 
        on_delete=models.CASCADE, 
        db_column='id_disciplina'
    )
    # Mantenha os outros campos (ex: semestre_ideal, obrigatoria, etc.)

    class Meta:
        db_table = 'matriz_disciplina'