from odoo import _, api, fields, models, tools

class EspaceRh(models.Model):

    _name = 'espace.rh'
    _description = 'Espace Rh'
    _inherit = ['mon.profil']
    
    name = fields.Char( default="Espace Administrateur")
    espace_rh_id = fields.Many2one('mon.profil', string='Espace Admin')
 

    def lister_fiche_signaletique(self):
        action = self.env['mon.profil'].show_mon_profil()
        return action
    
    def lister_cert_prise_service(self):
        action = self.env['certificat.prise.service'].show_certificat_prise_service()
        return action
    
    def lister_cert_reprise_service(self):
        action = self.env['reprise.service'].show_certificat_reprise_service()
        return action
    
    def lister_cert_travail(self):
        action = self.env['certificat.travail'].show_certificat_travail()
        return action
    
    def lister_cessation_definitive(self):
        action = self.env['cessation.service'].show_cessation_service()
        return action
    
    def lister_attestation_presence(self):
        action = self.env['attestation.presence'].show_attestation_presence()
        return action
    
    def lister_attestation_travail(self):
        action = self.env['attestation.travail'].show_attestation_travail()
        return action
    
    def lister_note_affectation(self):
        action = self.env['note.affectation'].show_note_affectation()
        return action
    
    nombre_fiche = fields.Integer(compute="_nombre_fiche_count", store=True,)
    @api.depends()
    def _nombre_fiche_count(self):
        for record in self:
            record.nombre_fiche = self.env['mon.profil'].search_count([])
    

        
        
