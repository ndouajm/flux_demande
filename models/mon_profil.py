import os
import base64
import qrcode
from io import BytesIO

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class MonProfil(models.Model):

    _name = 'mon.profil'
    _description = 'Mon Profil'
    
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    
    # etat Civil
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('publier', 'Publier'),
        ('accepte', 'Accepter'),
    ], string='Status', default='draft')
    
    employee_publier_id = fields.Many2one(
        'res.users',
        string='Employee Confirme',
        )
    
    employee_id = fields.Many2one(
        'res.users',
        string='Demandeur',
        default=lambda self: self.env.user,
        required=True,
        readonly=True,
    )
    
    confirm_date = fields.Date(
        default=fields.Date.context_today,
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
    
    #@api.multi
    def action_publier(self):
        for rec in self:
            rec.employee_publier_id = rec.employee_id.id
            rec.confirm_date = fields.Date.today()
            rec.state = 'publier' 
            if rec.alert_chef_cab_id:
                    message = f"Merci de valider la Fiche en attente de {rec.name} Matricule {rec.matricule}."
                    rec.message_post(body=message, partner_ids=[rec.alert_chef_cab_id.name.user_id.partner_id.id]) 

    #@api.multi
    def action_accept_fich(self):
        for rec in self:
            rec.state = 'accepte' 
            rec.confirm_date = fields.Date.today()
            responsible = rec.employee_publier_id
            responsible_email = responsible.email
            message = f"Votre fiche a bien été valider le {rec.confirm_date} par {rec.alert_chef_cab_id.name}."
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
            
    
    name = fields.Char( string="Nom", required=True,)
    prenom = fields.Char( string="Prenom")
    image_pro = fields.Binary('Image', max_width=250, max_height=250)
    nature_act_identite = fields.Char( string="Nature de l'acte d'identité")
    numero_act_identite = fields.Integer( string="N* De L'acte d'identité")
    date_naissance = fields.Date( string="Date De Naissance")
    lieu_naissance = fields.Char( string="Lieu De Naissance")
    date_deliv_act = fields.Date( string="Date D'etablissement De l'acte D'Identité")
    lieu_deliv_act = fields.Char( string="Lieu D'etablissement De l'acte D'Identité")
    

    
    nationalite_id = fields.Many2one(
        'res.country',
        string='Nationalité',
        default=lambda self: self.env['res.country'].search([('code', '=', 'CI')], limit=1),
        )
    
    sexe_id = fields.Selection([('m', 'Masculin'), ('f', 'Feminin')])
    
    nom_pere = fields.Char( string="Nom Du Père")
    prenom_pere = fields.Char( string="Prénom Du Père")
    
    nom_mere = fields.Char( string="Nom De La Mère")
    prenom_mere = fields.Char( string="Prenom De La Mère")
    
    situation_matrimo = fields.Selection([('c', 'Celibataire'), ('m', 'Marié'), ('v', 'Veuve')])
    nbr_enfants = fields.Integer( string="Nombre D'Enfants")

    # Renseignement Administractifs
    
    matricule = fields.Char( string="Matricule")
    
    grade = fields.Many2one('grade.fonctionnaire', string='Grade')
    
    emploie = fields.Many2one('hr.job', string='Emploi',)
     
    date_nomination = fields.Date( string="Date De nomination dans l'emploi")
    nature_act_n = fields.Char( string="Nature de l'act De nomination")
    numero_act_n = fields.Integer( string="Numero de l'act De nomination")
    date_service = fields.Date( string="Date De Prise De Service Dans L'administration")
    situation_mili = fields.Selection([('apte', 'Apte'), ('inapte', 'Inapte'), ('null', 'Sans Objet')])
    adresse_postal = fields.Char( string="Adresse postal")
    # telephone = fields.Integer( string="Telephone")
    telephone_bur = fields.Integer( string="Bur", default='+225')
    telephone_dom = fields.Integer( string="Dom", default='+225')
    telephone_cell = fields.Integer( string="Cell", default='+225')
    
    email_pro = fields.Char(string='e-mail pro', default='@telecom.gouv.ci')
    
    @api.constrains('email_pro')
    def _check_email_prefix(self):
        for record in self:
            if not record.email_pro.endswith('@telecom.gouv.ci'):
                raise ValidationError("Le préfixe de l'adresse email doit être '@telecom.gouv.ci'")
            
    
    email_perso = fields.Char( string="Email")
    
    # ministere_structure = fields.Char( string="Ministère Ou Structure")
    
    ministere_structure = fields.Many2one(
        'res.company',
        string='Ministère Ou Structure',
        default=lambda self: self.env['res.company'].search([('id', '=', 1)], limit=1),
        copy=True,
        # default=lambda self: self.env.user.company_id,
    )

    
    direction = fields.Many2one(
        'hr.department',
        string='Direction',
        required=False,
        copy=True,
        store=True,
        # readonly=False,
    )
    
    
    direction_date = fields.Date( string="Date d'Effet")
    
    service = fields.Char( string="Service")
    service_date = fields.Date( string="Date d'Effet")
    
    fonction = fields.Char( string="Fonction")
    fonction_date = fields.Date( string="Date d'Effet")
    
    localite = fields.Char( string="Localité")
    localite_date = fields.Date( string="Date d'Effet")
    
    specialite = fields.Char( string="Specialité")
    ministere_structure_origin = fields.Char( string="Ministère Et Structure D'Origine")
    
    experience_line_ids = fields.One2many(
        'experience.pro',
        'experience_id',
        string='experience pro line'
    )
    fonction_ant_line_ids = fields.One2many(
        'fonction.anterieure',
        'fonction_ante_id',
        string='Fonction Anterieure'
    )
    etude_formation_line_ids = fields.One2many(
        'etude.formation',
        'etude_formation_id',
        string='Etude Formation Proffessionnelle'
    )
    enfants_line_ids = fields.One2many(
        'nbr.enfants',
        'nbr_enfants_id',
        string='Enfants'
    )
    
    # personne en cas d'urgence 
    
    first_last_name_one = fields.Char()
    name_one_phone = fields.Integer()
    
    first_last_name_two = fields.Char()
    name_two_phone = fields.Integer()
    
    date_actu = fields.Date(
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )
 
    
    def show_mon_profil(model):
        user = model.env.user
        if user.has_group('flux_demande.group_flux_demande_admin'): 
            domain = []
        else:
            domain = [('create_uid', '=', user.id)]
        return {
            'name': _('Fiche Signalitique'),
            'domain': domain,
            'res_model': 'mon.profil',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    fichier = fields.Binary()

    def save_file(self):
        module_path = os.path.dirname(__file__)
        img_dir = os.path.join(module_path, 'img')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        file_path = os.path.join(img_dir, self.file_name)
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(self.fichier))
    
    def charger_fichier(self, file_data, file_name):
        mon_profil = self.env['mon.profil'].create({
            'fichier': file_data,
        })
        mon_profil.file_name = file_name
        mon_profil.save_file()
        
    # with open('\flux_demande\static\img\mon_fichier.jpg', 'rb') as f:
    #     file_data = f.read()

      
    qr_code = fields.Binary("QR Code", attachment=True)

    def generate_hr_qr(self):
        if self.matricule:
            if self.name:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                qr.add_data(self.name)
                qr.add_data('\n')
                qr.add_data(self.prenom)
                qr.add_data('\n')
                qr.add_data(self.matricule)
                qr.add_data('\n')
                qr.add_data(self.telephone_cell)
                qr.add_data('\n')
                qr.make(fit=True)
                img = qr.make_image()
                tmp = BytesIO()
                img.save(tmp, format="PNG")
                qr_img = base64.b64encode(tmp.getvalue())
                self.qr_code = qr_img
            else:
                raise UserError(_('Verifier si le Nom et le Matricule est saisir.'))
            

    nombre_fiche = fields.Integer(compute="_nombre_fiche_count", store=True)
    @api.depends()
    def _nombre_fiche_count(self):
        for record in self:
            record.nombre_fiche = self.env['mon.profil'].search_count([])
            
            