from odoo import _, api, fields, models, tools

class MotifDemande(models.Model):

    _name = 'flux.emploi'
    _description = 'Emploi'
    
    name = fields.Char()

