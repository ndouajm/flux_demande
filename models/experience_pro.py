from odoo import _, api, fields, models, tools

class ExperiencePro(models.Model):

    _name = 'experience.pro'
    _description = 'Experiences Proffesionnelles'
    
    

    experience_id = fields.Many2one(
        'mon.profil',
        string='Experiences Pro', 
    )
    
    date = fields.Date()
    emploie = fields.Char()
    structure = fields.Char()