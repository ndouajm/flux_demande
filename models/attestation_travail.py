
import base64
import qrcode
from io import BytesIO
from PIL import Image
from PIL import ImageDraw

from odoo import _, api, fields, models, tools

class attestationTravail(models.Model):

    _name = 'attestation.travail'
    _description = 'Attestattion De Travail'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char( default="Attestattion De Travail", readonly=True)
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        readonly=True,
    )

    matricule = fields.Char(related="employee_id.identification_id", readonly=True)
    direction = fields.Char(related="employee_id.department_id.name", readonly=True)
    emploi = fields.Char(related="employee_id.emploie.name", readonly=True)
    post_occuper = fields.Char(related="employee_id.job_id.name", readonly=True)
    date_prise_service = fields.Datetime(related="employee_id.create_date", readonly=True)
    date_start = fields.Date()

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
    
    
    date_start = fields.Date()
    date_end = fields.Date()
    
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
                    message = f"Merci de valider la demande en attente de {rec.name} publier par {rec.employee_publier_id.name}."
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


    def show_attestation_travail(model):
        user = model.env.user
        if user.has_group('flux_demande.group_flux_demande_admin'): # Vérifie si l'utilisateur est un admin
            domain = [] # afficher toutes les fiches
        else:
            domain = [('create_uid', '=', user.id)] # afficher seulement la fiche de l'utilisateur connecté
            
        return {
            'name': _('Attestation De Travail'),
            'domain': domain,
            'view_type': 'form',
            'res_model': 'attestation.travail',
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