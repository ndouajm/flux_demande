from odoo import _, api, fields, models, tools

class ConfigAlert(models.Model):

    _name = 'config.alert'
    _description = 'Configuration des Alertes'
    
    name = fields.Many2one(
        'hr.employee',
        string='Agent Rh',
        )
    
    actif = fields.Boolean( default= False)
    
    role = fields.Selection([('rh', 'Agent RH'),('drh','DRH')])
    
    agent_email = fields.Char( related='name.work_email' ,readonly=True)

