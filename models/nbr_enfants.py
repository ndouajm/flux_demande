from odoo import _, api, fields, models, tools

class NombreEnfants(models.Model):

    _name = 'nbr.enfants'
    _description = 'Nombre D"Enfants'
    
    name = fields.Char()
    
    nom_prenom = fields.Char()
    birthday = fields.Date()
    lieu_naissance = fields.Char()
    sexe_enfants = fields.Selection([('m', 'M'), ('f', 'F')])

    nbr_enfants_id = fields.Many2one(
        'mon.profil',
        string='Enfants', 
    )