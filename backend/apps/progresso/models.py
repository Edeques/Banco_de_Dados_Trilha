from django.db import models

# CLASSE 15: Progresso
class Progresso(models.Model):
    id_progresso = models.AutoField(primary_key=True, db_column='id_progresso')
    id_usuario = models.ForeignKey( # Confira no Supabase se a coluna é id_usuario ou id_aluno
        'usuarios.Aluno', 
        on_delete=models.CASCADE, 
        db_column='id_usuario'
    )
    id_disciplina = models.ForeignKey(
        'disciplinas.Disciplina', 
        on_delete=models.CASCADE, 
        db_column='id_disciplina'
    )
    # Mantenha os outros campos (ex: status, nota, semestre_cursado, etc.)

    class Meta:
        db_table = 'progresso'