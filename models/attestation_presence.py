from odoo import _, api, fields, models, tools

class AttestationPresence(models.Model):

    _name = 'attestation.presence'
    _description = 'Attestation De Presence'
    
    _inherit = ['mail.thread']
    
    name = fields.Char( default="Attestation De Presence", readonly=True)
    

    employee_id = fields.Many2one(
        'mon.profil',
        string='Demandeur',
        default=lambda self: self.env['mon.profil'].search([('create_uid', '=', self.env.uid)], limit=1),
        required=True,
        readonly=True,
    )
    
    employee_publier_id = fields.Many2one(
        'res.users',
        string='Employee Confirme',
        )
    
    confirm_employee_id = fields.Many2one(
        'res.users',
        string='Demandeur',
        default=lambda self: self.env.user,
        required=True,
        readonly=True,
    )

    matricule = fields.Char(related="employee_id.matricule", readonly=True)
    emploi = fields.Char(related="employee_id.emploie.name", readonly=True)
    direction = fields.Char(related="employee_id.direction.name", readonly=False)

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
    
    alert_chef_cab_id = fields.Many2one(
        'config.alert',
        default=lambda self: self.env['config.alert'].search([('actif', '=', True)], limit=1),
        required=True,
        readonly=True,
        string='Agent RH',
        )
    
    confirm_date = fields.Date(
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )
    
    
#@api.multi
    def action_confim(self):
        for rec in self:
            rec.state = 'drh_approval'
            rec.employee_publier_id = rec.confirm_employee_id.id
            rec.confirm_date = fields.Date.today()
            if rec.alert_chef_cab_id:
                    message = f"Merci de valider la Fiche en attente de {rec.name} Matricule {rec.matricule}."
                    rec.message_post(body=message, partner_ids=[rec.alert_chef_cab_id.name.user_id.partner_id.id])  
  
#@api.multi
    def action_approval_drh(self):
        for rec in self:
            rec.state = 'done'
            rec.confirm_date = fields.Date.today()
            responsible = rec.employee_publier_id
            responsible_email = responsible.email
            message = f"Votre {rec.name}  a bien été Approuver le {rec.confirm_date} par {rec.alert_chef_cab_id.name}."
            values = {
                'email_from': self.env.user.email,
                'email_to': responsible_email,
                'subject': 'Profil Accepté',
                'body_html': message,
            }
            # Créer l'objet mail.mail et envoyer l'e-mail
            self.env['mail.mail'].create(values).send()  
               
#@api.multi
    def action_annuler(self):
        for rec in self:
            rec.state = 'draft'     
            
 

    def show_attestation_presence(model):
        user = model.env.user
        if user.has_group('flux_demande.group_flux_demande_admin'): # Vérifie si l'utilisateur est un admin
            domain = [] # afficher toutes les fiches
        else:
            domain = [('create_uid', '=', user.id)] # afficher seulement la fiche de l'utilisateur connecté
            
        return {
            'name': _('Attestation De Presence'),
            'domain': domain,
            'view_type': 'form',
            'res_model': 'attestation.presence',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
