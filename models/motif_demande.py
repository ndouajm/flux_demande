from odoo import _, api, fields, models, tools

class MotifDemande(models.Model):

    _name = 'motif.demande'
    _description = 'Motif De La Demande'
    
    name = fields.Char()

