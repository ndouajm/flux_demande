from odoo import _, api, fields, models, tools

class TypeDocument(models.Model):

    _name = 'type.document'
    _description = 'Type De Document'
    
    name = fields.Char( string="Libellé Du Document")

