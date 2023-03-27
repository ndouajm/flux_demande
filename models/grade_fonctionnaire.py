from odoo import _, api, fields, models, tools

class GradeFonctionnaire(models.Model):

    _name = 'grade.fonctionnaire'
    _description = 'Grade Du Fonctionnaire'
    
    
    name = fields.Char( string="libellé Du Grade")

