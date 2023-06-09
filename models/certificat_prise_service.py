
import base64
import qrcode
from io import BytesIO
from PIL import Image
from PIL import ImageDraw

from odoo import _, api, fields, models, tools

class CertificatPriseService(models.Model):

    _name = 'certificat.prise.service'
    _description = 'Certificat De Prise De Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char( default="Certificat De Prise De Service", readonly=True)
    
    @api.model
    def generate_sequence(self):
        prefix = 'CPS-'
        sequence = self.env['ir.sequence'].next_by_code('note.affectation.sequence') or '/'
        numero = f'{prefix}{sequence}'
        return numero

    numero = fields.Char(string='Numéro', default=generate_sequence, readonly=True, store=True)
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        readonly=True,
        copy=True,
    )

    emploie = fields.Char(related="employee_id.emploie.name", readonly=True)
    post_occuper = fields.Char(related="employee_id.fonction.name", readonly=True)
    direction = fields.Char(related="employee_id.department_id.name", readonly=True)
    matricule = fields.Char(related="employee_id.identification_id", readonly=True)
   
    date_start = fields.Datetime(related="employee_id.create_date", readonly=True)

    request_date = fields.Date(
        string='Date De Demande',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )

    note = fields.Text()

    report_date = fields.Date(
        default=fields.Date.context_today,
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
    
    signature = fields.Char()
      
# demande valider
    def liste_certificat_prise_service(model):
        user = model.env.user
        return {
                'name': _('Mes Certificat De prise De Service'),
                'domain': [('create_uid', '=', user.id)],
                'res_model': 'certificat.prise.service',
                'view_id': False,
                'view_mode': 'tree',
                'type': 'ir.actions.act_window',
            }
        
    def show_certificat_prise_service(model):
        user = model.env.user
        if user.has_group('flux_demande.group_flux_demande_admin'): # Vérifie si l'utilisateur est un admin
            domain = [] # afficher toutes les fiches
        else:
            domain = [('create_uid', '=', user.id)] # afficher seulement la fiche de l'utilisateur connecté
            
        return {
            'name': _('Certificat De prise De Service'),
            'domain': domain,
            'res_model': 'certificat.prise.service',
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

            qr.add_data(f"Document : {self.name}\nNom de l'Agent : {self.employee_id.name}\nPoste occupé : {self.post_occuper}\nMatricule : {self.matricule}")
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
            
         # def generate_hr_qr(self):
    #     if self.name:
    #         qr = qrcode.QRCode(
    #             version=1,
    #             error_correction=qrcode.constants.ERROR_CORRECT_L,
    #             box_size=10,
    #             border=4,
    #         )

    #         qr.add_data(f"Document : {self.name}\nNom de l'Agent : {self.employee_id}\nPoste occupé : {self.post_occuper}")
    #         qr.make(fit=True)
    #         img = qr.make_image()
    #         tmp = BytesIO()
    #         img.save(tmp, format="PNG")
    #         qr_img = base64.b64encode(tmp.getvalue())
    #         self.qr_code = qr_img

