import base64
import qrcode
from io import BytesIO
from PIL import Image
from PIL import ImageDraw

from odoo import _, api, fields, models, tools

class NoteAffectation(models.Model):

    _name = 'note.affectation'
    _description = 'Note D"Affectation'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char( default="Note D'Affectation", readonly=True)
    
    
    @api.model
    def generate_sequence(self):
        prefix = 'NA-'
        sequence = self.env['ir.sequence'].next_by_code('note.affectation.sequence') or '/'
        numero = f'{prefix}{sequence}'
        return numero

    numero = fields.Char(string='Numéro', default=generate_sequence, readonly=True, store=True)
    signature = fields.Char()

    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        readonly=True,
    )
    
    typ_note = fields.Selection([
        ('int', 'Interne'),
        ('ext', 'Externe')],
        string="Type de Demade"
    )

    
    matricule = fields.Char(related="employee_id.identification_id", readonly=True)
    direction = fields.Char(related="employee_id.department_id.name", readonly=True)
    emploi = fields.Char(related="employee_id.emploie.name", readonly=True)
    post_occuper = fields.Char(related="employee_id.fonction.name", readonly=True)
    date_prise_service = fields.Datetime(related="employee_id.create_date")


    request_date = fields.Date(
        string='Date De Demande',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )
    
    note = fields.Text()
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('drh_approval', 'Traitement agent RH'),
        ('drh_sign', 'Attente de Signature DRH'),
        ('done', 'Valider'),
        ('reject', 'Rejeter'),
    ], string='state', default='draft')
    
    
    date_start = fields.Date()
    date_end = fields.Date()
    
    user_demande_id = fields.Many2one(
        'res.users',
        string='user',
        default=lambda self: self.env.user,
        required=True,
        readonly=True,
    )
     
    employee_publier_id = fields.Many2one('res.users', string='Employee Confirme')
    confirm_date = fields.Date( default=fields.Date.context_today)
    
    validateur_rh_id = fields.Many2one(
        'config.alert',
        default=lambda self: self.env['config.alert'].search([('actif', '=', True), ('role', '=', 'rh')], limit=1),
        required=True,
        readonly=True,
        string='Agent RH',
    )
     
    approval_agent_rh_id = fields.Many2one( 'res.users', string='Agent Rh Approbateur',)
    approval_date = fields.Date( default=fields.Date.context_today)
    
    agent_drh_id = fields.Many2one(
        'config.alert',
        default=lambda self: self.env['config.alert'].search([('actif', '=', True), ('role', '=','drh')], limit=1),
        required=True,
        readonly=True,
        string='DRH',
    )
    drh_signed = fields.Many2one('res.users', string='Agent DRH ')
    signature_drh_date = fields.Date( default=fields.Date.context_today,readonly=True,)
   
    
    
#@api.multi
    def action_confim(self):
        for rec in self:
            rec.state = 'drh_approval'
            rec.employee_publier_id = rec.user_demande_id.id
            rec.confirm_date = fields.Date.today()
            if rec.validateur_rh_id:
                    message = f"Merci de valider la demande d'{rec.name} Numero {rec.numero} en attente de validation."
                    rec.message_post(body=message, partner_ids=[rec.validateur_rh_id.name.user_id.partner_id.id])
                    
#@api.multi
    def action_approval_rh(self):
        for rec in self:
            rec.state = 'drh_sign'
            rec.approval_agent_rh_id = rec.user_demande_id.id
            rec.approval_date = fields.Date.today()
            if rec.agent_drh_id:
                    message = f"Merci de signer la demande d'{rec.name} Numero {rec.numero} en attente de signature."
                    rec.message_post(body=message, partner_ids=[rec.agent_drh_id.name.user_id.partner_id.id]) 
  
#@api.multi
    def action_signature_drh(self):
        for rec in self:
            rec.state = 'done'
            rec.signature_drh_date = fields.Date.today()
            responsable = rec.employee_publier_id
            responsible_email = responsable.email
            message = f"Votre {rec.name}  Numero {rec.numero} a bien été Valider le {rec.signature_drh_date}."
            values = {
                'email_from': self.env.user.email,
                'email_to': responsible_email,
                'subject': 'Note d"Affectation Validé',
                'body_html': message,
            }
            # Créer l'objet mail.mail et envoyer l'e-mail
            self.env['mail.mail'].create(values).send() 
               
#@api.multi
    def action_annuler(self):
        for rec in self:
            rec.state = 'draft'     
            
#@api.multi
    def action_reject(self):
        for rec in self:
            rec.state = 'reject'
            responsable = rec.employee_publier_id
            responsible_email = responsable.email
            message = f"Votre {rec.name} Numero {rec.numero} a été rejetée Contacter l'administration pour en savoir plus Merci ."
            values = {
                'email_from': self.env.user.email,
                'email_to': responsible_email,
                'subject': 'Note D"Affectation Rejeté',
                'body_html': message,
            }
            # Créer l'objet mail.mail et envoyer l'e-mail
            self.env['mail.mail'].create(values).send()   

    def show_note_affectation(model):
        user = model.env.user
        if user.has_group('flux_demande.group_flux_demande_admin'): # Vérifie si l'utilisateur est un admin
            domain = [] # afficher toutes les fiches
        else:
            domain = [('create_uid', '=', user.id)] # afficher seulement la fiche de l'utilisateur connecté
            
        return {
            'name': _('Note d\'Affectation'),
            'domain': domain,
            'view_type': 'form',
            'res_model': 'note.affectation',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    qr_code = fields.Binary("QR Code", attachment=True)

    @api.model
    def create(self, vals):
        employee = super().create(vals)
        employee.generate_hr_qr()
        return employee

    def write(self, vals):
        res = super().write(vals)
        if 'name' in vals:
            self.generate_hr_qr()
        return res
    
    
    def generate_hr_qr(self):
        if self.name:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(f"Document : {self.name}\nNom de l'Agent : {self.employee_id}\nPoste occupé : {self.post_occuper}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="#ffffff", back_color="#ff9900")
            logo_size = 100 # La taille du logo
            logo_path = 'C:/Program Files/Odoo 14.0.20230307/server/odoo/addons/flux_demande/static/description/amoirie.png'  # Le chemin vers le logo
            logo = Image.open(logo_path).resize((logo_size, logo_size), Image.ANTIALIAS).convert('RGBA')
            position = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            img.paste(logo, position, logo)
            tmp = BytesIO()
            img.save(tmp, format="PNG")
            qr_img = base64.b64encode(tmp.getvalue())
            self.qr_code = qr_img

