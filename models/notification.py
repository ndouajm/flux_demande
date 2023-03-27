from odoo import _, api, fields, models, tools

class Notification(models.Model):
    _name = 'notification'
    _inherit = 'mail.message'

    name = fields.Char()