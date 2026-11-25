from django.db import models

# CLASSE 5: Disciplina
class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True, db_column='id_disciplina')
    # Mantenha os campos de codigo, nome, carga_horaria, etc. que já estão no seu arquivo

    class Meta:
        db_table = 'disciplina'


# CLASSE 6: PreRequisito
class PreRequisito(models.Model):
    id_disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_disciplina',
        related_name='requisitos'
    )
    id_pre_requisito = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        db_column='id_pre_requisito', # Confira no Supabase se o nome da 2ª coluna é exatamente esse
        related_name='eh_requisito_de'
    )

    class Meta:
        db_table = 'pre_requisito'
        unique_together = (('id_disciplina', 'id_pre_requisito'),)