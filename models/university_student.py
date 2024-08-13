# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana Jabin MP (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import api, fields, models, _


class UniversityStudent(models.Model):
    """To keep records of university student details"""
    _name = 'university.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    _description = 'University student records'

    @api.model
    def create(self, vals):
        """ This method overrides the create method to assign a sequence number
            to the newly created record.
           :param vals (dict): Dictionary containing the field values for the
                                new university student record.
           :returns class: university.student The created university student
                            record."""
        vals['admission_no'] = self.env['ir.sequence'].next_by_code(
            'university.student')
        res = super(UniversityStudent, self).create(vals)
        return res

    partner_id = fields.Many2one(
        'res.partner', string='Partenaire', help="Partenaire de l'étudiant",
        required=True, ondelete="cascade")
    middle_name = fields.Char(string='Deuxième prénom',
                             help="Deuxième prénom de l'étudiant")
    last_name = fields.Char(string='Prènom', help=" le prenom   l'étudiant")
    application_no = fields.Char(string="Numéro de demande",
                                help="Numéro de demande de l'étudiant")
    date_of_birth = fields.Date(string="Date de naissance", requird=True,
                                help="Détails de la date de naissance")
    guardian_id = fields.Many2one('res.partner', string="Tuteur",
                                help="Détails du tuteur de l'étudiant",
                                domain=[('is_parent', '=', True)])
    father_name = fields.Char(string="Père", help="Détails sur le père de l'étudiant")
    mother_name = fields.Char(string="Mère", help="Détails sur la mère de l'étudiant")
    semester_id = fields.Many2one('university.semester',
                                string="Semestre",
                                help="Semestre de l'étudiant")
    department_id = fields.Many2one(related='semester_id.department_id',
                                    help="Département du semestre",
                                    string="Département")
    course_id = fields.Many2one(related='department_id.course_id',
                                help="Cours dans le département",
                                string="Cours")
    admission_no = fields.Char(string="Numéro d'admission", readonly=True,
                            help="Numéro d'admission de l'étudiant")
    gender = fields.Selection([('male', 'Homme'),
                            ('female', 'Femme'),
                            ('other', 'Autre')],
                            help="Détails sur le sexe de l'étudiant",
                            string='Sexe', required=True, default='male',
                            track_visibility='onchange')
    blood_group = fields.Selection([('a+', 'A+'),
                                    ('a-', 'A-'),
                                    ('b+', 'B+'),
                                    ('o+', 'O+'),
                                    ('o-', 'O-'),
                                    ('ab-', 'AB-'),
                                    ('ab+', 'AB+')],
                                string='Groupe sanguin', required=True,
                                help="Détails sur le groupe sanguin de l'étudiant",
                                default='a+',
                                track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Entreprise',
                                help="Entreprise")
    per_street = fields.Char(string="Rue", help="Adresse de la rue")
    per_street2 = fields.Char(string="Rue 2", help="Adresse de la rue 2")
    per_zip = fields.Char(change_default=True, string="Code postal",
                        help="Détails du code postal/de la boîte postale")
    per_city = fields.Char(string="Ville", help="Ville de résidence de l'étudiant")
    per_state_id = fields.Many2one("res.country.state",
                                string='État', help="État",
                                ondelete='restrict')
    per_country_id = fields.Many2one('res.country',
                                    string='Pays',
                                    help="Nationalité de l'étudiant",
                                    ondelete='restrict')
    mother_tongue = fields.Char(string="Langue maternelle",
                                help="Langue maternelle de l'étudiant")
    caste = fields.Char(string="Caste",
                        help="Détails sur la caste de l'étudiant")
    religion = fields.Char(string="Religion",
                        help="Détails sur la religion de l'étudiant")
    is_same_address = fields.Boolean(string="Adresse identique ?",
                                    help="Activez si l'étudiant a une seule adresse")
    nationality_id = fields.Many2one('res.country',
                                    string='Nationalité',
                                    help="Nationalité de l'étudiant",
                                    ondelete='restrict')
    application_id = fields.Many2one('university.application',
                                    help="Numéro de demande de l'étudiant",
                                    string="Numéro de demande")
    user_id = fields.Many2one('res.users', string="Utilisateur",
                            readonly=True,
                            help="Utilisateur associé à l'étudiant")
    batch_id = fields.Many2one('university.batch', string="Promotion",
                            help="Relation avec les promotions de l'université")
    academic_year_id = fields.Many2one('university.academic.year',
                                    string="Année académique",
                                    help="Année académique de l'étudiant")

    def action_student_documents(self):
        """ Open the documents submitted by the student along with the admission
            application. This method retrieves the documents associated with
            the admission application linked to the current student record.
            :returns dict: A dictionary defining the action to open the
                            'university.document' records."""
        self.ensure_one()
        if self.application_id.id:
            documents_list = self.env['university.document'].search(
                [('application_ref_id', '=', self.application_id.id)]).mapped(
                'id')
            return {
                'domain': [('id', 'in', documents_list)],
                'name': _('Documents'),
                'view_mode': 'tree,form',
                'res_model': 'university.document',
                'view_id': False,
                'context': {'application_ref_id': self.application_id.id},
                'type': 'ir.actions.act_window'
            }
