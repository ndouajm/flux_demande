from odoo import _, api, fields, models, tools

class EtudeFormation(models.Model):

    _name = 'etude.formation'
    _description = 'Etude Formation Professionnelles'
    
    diplome = fields.Char()
    year_obtention = fields.Date()
    etabli_frequent = fields.Char()
    ville_pays = fields.Char()
    
    etude_formation_id = fields.Many2one(
        'mon.profil',
        string='Etude Formation Proffessionnelles', 
    )

