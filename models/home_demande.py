from odoo import _, api, fields, models, tools

class HomeModel(models.Model):

    _name = 'home.demande'
    _description = 'Home Demande'
    
    
    name = fields.Char()

