from odoo import _, api, fields, models, tools


class FluxDemande(models.Model):

    _name = 'flux.demande'
    _description = 'Flux de Demande'

    _inherit = ['mail.thread','mail.activity.mixin']
    
    name = fields.Char()
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        readonly=True,
        copy=True,
    )
    
    type_document_id = fields.Many2one(
        'type.document',
        string='Type De Document',
        )
    
    request_date = fields.Date(
        string='Date De Demande',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )
    
    note = fields.Text()
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('drh_approval', 'Attente de Validation DRH'),
        ('done', 'Valider'),
    ], string='state', default='draft')
    
    motif_id = fields.Many2one(
        'motif.demande',
        string='Motif De la Demande',
        )
    
    date_start = fields.Date()
    date_end = fields.Date()

#@api.multi
    def action_confim(self):
        for rec in self:
            rec.state = 'drh_approval'
            
#@api.multi
    def action_approval_drh(self):
        for rec in self:
            rec.state = 'done'  
               
    #@api.multi
    def action_annuler(self):
        for rec in self:
            rec.state = 'draft'     

        