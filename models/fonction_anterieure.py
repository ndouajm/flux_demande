from odoo import _, api, fields, models, tools

class Fonctionanterieures(models.Model):

    _name = 'fonction.anterieure'
    _description = 'Fonction Anterieure'
    
    fonction_ante_id = fields.Many2one(
        'mon.profil',
        string='Fonction Anterieure', 
    )
    
    f_date_start = fields.Date()
    f_date_end = fields.Date()
    designation_post = fields.Char()
    structure = fields.Char()

