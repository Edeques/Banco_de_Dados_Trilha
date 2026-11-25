from django.db import models

# CLASSE 12: Planejamento
class Planejamento(models.Model):
    id_planejamento = models.AutoField(primary_key=True, db_column='id_planejamento')
    id_usuario = models.ForeignKey( # Confira no Supabase se a coluna é id_usuario ou id_aluno
        'usuarios.Aluno', 
        on_delete=models.CASCADE, 
        db_column='id_usuario'
    )
    # Mantenha os outros campos (ex: titulo, data_criacao, etc.)

    class Meta:
        db_table = 'planejamento'


# CLASSE 13: SemestrePlanejamento
class SemestrePlanejamento(models.Model):
    id_semestre_planejamento = models.AutoField(primary_key=True, db_column='id_semestre_planejamento')
    id_planejamento = models.ForeignKey(
        Planejamento, 
        on_delete=models.CASCADE, 
        db_column='id_planejamento'
    )
    # Mantenha os outros campos (ex: numero_semestre, periodo_letivo, etc.)

    class Meta:
        db_table = 'semestre_planejamento'


# CLASSE 14: ItemPlanejamento
class ItemPlanejamento(models.Model):
    id_item_planejamento = models.AutoField(primary_key=True, db_column='id_item_planejamento')
    id_semestre_planejamento = models.ForeignKey(
        SemestrePlanejamento, 
        on_delete=models.CASCADE, 
        db_column='id_semestre_planejamento'
    )
    id_disciplina = models.ForeignKey(
        'disciplinas.Disciplina', 
        on_delete=models.CASCADE, 
        db_column='id_disciplina'
    )
    # Caso tenha ligação opcional com ItemOferta, adicione:
    # id_item_oferta = models.ForeignKey('ofertas.ItemOferta', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_item_oferta')

    class Meta:
        db_table = 'item_planejamento'