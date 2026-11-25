from django.db import models

# CLASSE 9: Oferta
class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True, db_column='id_oferta')
    id_curso = models.ForeignKey(
        'cursos.Curso', 
        on_delete=models.CASCADE, 
        db_column='id_curso'
    )
    # Mantenha os outros campos (ex: semestre_letivo, status, etc.)

    class Meta:
        db_table = 'oferta'


# CLASSE 10: ItemOferta
class ItemOferta(models.Model):
    id_item_oferta = models.AutoField(primary_key=True, db_column='id_item_oferta')
    id_oferta = models.ForeignKey(
        Oferta, 
        on_delete=models.CASCADE, 
        db_column='id_oferta'
    )
    id_disciplina = models.ForeignKey(
        'disciplinas.Disciplina', 
        on_delete=models.CASCADE, 
        db_column='id_disciplina'
    )
    # Mantenha os outros campos (ex: turma, professor, vagas, etc.)

    class Meta:
        db_table = 'item_oferta'


# CLASSE 11: Encontro
class Encontro(models.Model):
    id_encontro = models.AutoField(primary_key=True, db_column='id_encontro')
    id_item_oferta = models.ForeignKey(
        ItemOferta, 
        on_delete=models.CASCADE, 
        db_column='id_item_oferta'
    )
    # Mantenha os outros campos (ex: dia_semana, hora_inicio, hora_fim, sala, etc.)

    class Meta:
        db_table = 'encontro'