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
from odoo.exceptions import ValidationError


class UniversityApplication(models.Model):
    """ For managing student applications to the courses of the university"""
    _name = 'university.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Applications for the admission'

    @api.model
    def create(self, vals):
        """Overriding the create method and assigning
            the sequence for the record"""
        if vals.get('application_no', _('New')) == _('New'):
            vals['application_no'] = self.env['ir.sequence'].next_by_code(
                'university.application') or _('New')
        res = super(UniversityApplication, self).create(vals)
        return res

    name = fields.Char(string='Nom', required=True,
                       help="Entrez le nom de l'étudiant")
    # middle_name = fields.Char(string='Middle Name',
    #                           help="Enter Middle name of Student")
    last_name = fields.Char(string='Prénom',
                            help="Entrez le prénom de l'étudiant")
    image = fields.Binary(string='Image',
                          attachment=True,
                          help="Fournir l'image de l'étudiant")
    academic_year_id = fields.Many2one(
        'university.academic.year',
        string="Année académique",
        help="Choisissez l'année académique pour laquelle l'admission est choisie")
    course_id = fields.Many2one(
        'university.course', string="Cours",
        required=True,
        help="Entrez le cours pour lequel l'admission est demandée")
    department_ids = fields.Many2many(
        'university.department', string="Département",
        compute="_compute_department_ids",
        help="Entrez le département pour lequel l'admission est demandée")
    department_id = fields.Many2one(
        'university.department', string="Département",
        required=True,
        help="Entrez le département pour lequel l'admission est demandée")
    semester_ids = fields.Many2many('university.semester',
                                    string="Semester",
                                    compute="_compute_semester_ids",
                                    help="Entrez le semestre pour lequel l'admission est demandée")
    semester_id = fields.Many2one('university.semester',
                                  string="Semester", required=True,
                                  help="Entrez le semestre pour lequel l'admission est demandée")
    batch_ids = fields.Many2many('university.batch',
                                 string="Batch", compute="_compute_batch_ids",
                                 help="Enter batch to which the "
                                      "admission is seeking")
    batch_id = fields.Many2one('university.batch', string="Batch",
                               help="Enter batch to which the "
                                    "admission is seeking")
    admission_date = fields.Datetime('Admission Date',
                                     help="Date de prise en charge de l'admission",
                                     default=fields.Datetime.now,
                                     required=True)
    application_no = fields.Char(string='Numéro de demande',
                             help="Numéro de demande pour la nouvelle admission",
                                 readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company',
                                 help="Company of the application",
                                 default=lambda self: self.env.user.company_id)
    email = fields.Char(string="Email", required=True,
                        help="Entrez l'adresse e-mail à des fins de contact")
    phone = fields.Char(string="téléphone",
                        help="Entrez le numéro de téléphone à des fins de contact")
    mobile = fields.Char(string="Mobile", required=True,
                         help="Entrez le numéro de mobile à des fins de contact")
    nationality_id = fields.Many2one('res.country',
                                     string='Nationalité', ondelete='restrict',
                                     help="Choisissez la nationalité")
    mother_tongue = fields.Char(string="Langue maternelle",
                                help="Entrez la langue maternelle de l'étudiant")
    religion = fields.Char(string="Religion",
                           help="Ma religion est")
    caste = fields.Char(string="Caste",
                        help="Ma caste est")
    street = fields.Char(string='Rue', help="Entrez la rue")
    street2 = fields.Char(string='Street2', help="Entrez la rue")
    zip = fields.Char(change_default=True, string='Code postal',
                      help="Entrez le code postal")
    city = fields.Char(string='Ville', help="Entrez le nom de la ville")
    state_id = fields.Many2one("res.country.state", string="L'eta",
                               ondelete='restrict',
                               help="Choisissez l'état d'où vous venez")
    country_id = fields.Many2one('res.country', string='Pays',
                                 ondelete='restrict',
                                 help="Choisissez le pays")
    is_same_address = fields.Boolean(
        string="Adresse permanente identique à ci-dessus",
        default=True,
        help="Cochez la case si l'adresse actuelle et l'adresse permanente sont identiques")
    per_street = fields.Char(string='Rue', help="Entrez la rue")
    per_street2 = fields.Char(string='Rue2', help="Entrez la rue")
    per_zip = fields.Char(change_default=True, string='Code postal',
                          help="Entrez le code postal")
    per_city = fields.Char(string='Ville', help="Entrez le nom de la ville")
    per_state_id = fields.Many2one("res.country.state",
                                   string="L'etat", ondelete='restrict',
                                   help="Sélectionnez l'état d'où vous venez")
    per_country_id = fields.Many2one('res.country',
                                     string='Pays', ondelete='restrict',
                                     help="Sélectionnez le pays")
    date_of_birth = fields.Date(string="Date de naissance", required=True,
                                help="Entrez votre date de naissance")
    guardian_id = fields.Many2one('res.partner', string="Gardien",
                                  domain=[('is_parent', '=', True)],
                                  required=True,
                                  help="Indiquez qui s'occupera de vous")
    description = fields.Text(string="Note",
                              help="Description about the application")
    father_name = fields.Char(string="Père", help="Mon père est")
    mother_name = fields.Char(string="Mère ", help="Ma mère s'appelle")
    active = fields.Boolean(string='Active', default=True,
                            help="L'application est-elle active ou non")
    document_count = fields.Integer(compute='_compute_document_count',
                                    string='# Documents',
                                    help="Nombre de documents de candidature")
    verified_by_id = fields.Many2one('res.users',
                                     string='Vérifié par',
                                     help="Le document est vérifié par")
    reject_reason = fields.Many2one('reject.reason',
                                    string='Raison du rejet',
                                    help="La candidature est rejetée parce que")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='sexe ', required=True, default='male',
        track_visibility='onchange',
        help="Votre sexe est")
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')], string='Groupe sanguin',
        required=True, default='a+', track_visibility='onchange',
        help="Votre groupe sanguin est")
    state = fields.Selection([('draft', 'Brouillon'),
                              ('verification', 'Vérifier'),
                              ('approve', 'Approuver'), ('reject', 'Rejeté'),
                              ('done', 'Terminé')], string="L'ètat", required=True,
                             default='draft', track_visibility='onchange',
                             help="Statut de la candidature")
    prev_institute = fields.Char('Previous Institute',
                                 help="Institution précédemment étudiée",)
    prev_course = fields.Char('Previous Course',
                              help="Cours précédemment étudié")
    prev_result = fields.Char('Previous Result',
                              help="Résultat précédemment obtenu")

    def _compute_document_count(self):
        """Return the count of the documents provided"""
        for rec in self:
            rec.document_count = self.env['university.document'].search_count(
                [('application_ref_id', '=', rec.id)])

    def action_document_view(self):
        """ smart button action of viewing list of documents of application
            :return dict: the list of documents view
        """
        return {
            'name': _('Documents'),
            'domain': [('application_ref_id', '=', self.id)],
            'res_model': 'university.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'context': {'default_application_ref_id': self.id}
        }

    def action_send_verification(self):
        """Button action for sending the application for the verification"""
        for rec in self:
            if not self.env['university.document'].search(
                    [('application_ref_id', '=', rec.id)]):
                raise ValidationError(_("Aucun document fourni"))
            rec.write({
                'state': 'verification'
            })

    def action_verify_application(self):
        """ This method checks the status of documents related to the student
            application. If no documents are provided or if the provided
            documents are not in the 'done' state, it raises a validation error
            Otherwise, it updates the verification status of the application
            and approves it.

            :raises ValidationError: If all documents are not verified or no
                documents are provided.
        """
        for rec in self:
            doc_status = self.env['university.document'].search(
                [('application_ref_id', '=', rec.id)]).mapped('state')
            if doc_status:
                if all(state in 'done' for state in doc_status):
                    rec.write({
                        'verified_by_id': self.env.uid,
                        'state': 'approve'
                    })
                else:
                    raise ValidationError(
                        _('Tous les documents ne sont pas encore vérifiés, '
                          'Veuillez compléter la vérification'))
            else:
                raise ValidationError(_('Aucun document fourni'))

    def action_reject(self):
        """This method updates the state of the student application to 'reject',
            indicating that the application has been rejected for admission.
        """
        for rec in self:
            rec.write({
                'state': 'reject'
            })

    def action_create_student(self):
        """ This method creates a new student record using the data from the
             application.It populates the student record with the relevant
             information. It also assigns a user login for the student.

            :returns dict: A dictionary containing the information required
                            to open the student form view."""
        for rec in self:
            values = {
                'name': rec.name,
                'last_name': rec.last_name,
                'middle_name': rec.middle_name,
                'application_id': rec.id,
                'father_name': rec.father_name,
                'mother_name': rec.mother_name,
                'guardian_id': rec.guardian_id.id,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'state_id': rec.state_id.id,
                'country_id': rec.country_id.id,
                'zip': rec.zip,
                'is_same_address': rec.is_same_address,
                'per_street': rec.per_street,
                'per_street2': rec.per_street2,
                'per_city': rec.per_city,
                'per_state_id': rec.per_state_id.id,
                'per_country_id': rec.per_country_id.id,
                'per_zip': rec.per_zip,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'blood_group': rec.blood_group,
                'nationality_id': rec.nationality_id.id,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image_1920': rec.image,
                'is_student': True,
                'religion': rec.religion,
                'caste': rec.caste,
                'mother_tongue': rec.mother_tongue,
                'semester_id': rec.semester_id.id,
                'academic_year_id': rec.academic_year_id.id,
                'company_id': rec.company_id.id,
                'batch_id': rec.batch_id.id,
            }
            if not rec.is_same_address:
                pass
            else:
                values.update({
                    'per_street': rec.street,
                    'per_street2': rec.street2,
                    'per_city': rec.city,
                    'per_state_id': rec.state_id.id,
                    'per_country_id': rec.country_id.id,
                    'per_zip': rec.zip,
                })
            student = self.env['university.student'].create(values)
            student.user_id = self.env['res.users'].create({
                'name': student.name,
                'login': student.email,
                'partner_id': student.partner_id.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
            })
            rec.write({
                'state': 'done'
            })
            return {
                'name': _('Student'),
                'view_mode': 'form',
                'res_model': 'university.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }

    @api.depends('course_id')
    def _compute_department_ids(self):
        """ To find the departments in the selected course and assign them
            to department_ids field for setting domain for department_id field
        """
        for rec in self:
            rec.department_ids = self.env['university.department'].search(
                [('course_id', '=',
                  self.course_id.id)]).ids if rec.course_id else False

    @api.depends('department_id')
    def _compute_semester_ids(self):
        """ To find the semester in the selected department and assign them
            to semester_ids field for setting domain for semester_id field"""
        for rec in self:
            rec.semester_ids = self.env['university.semester'].search(
                [('department_id', '=',
                  self.department_id.id)]).ids if rec.department_id else False

    @api.depends('semester_id')
    def _compute_batch_ids(self):
        """ To find the batch in the selected semester and assign them
            to batch_ids field."""
        for rec in self:
            rec.batch_ids = self.env['university.batch'].search(
                [('semester_id', '=',
                  self.semester_id.id)]).ids if rec.semester_id else False

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        """ It checks if the provided date of birth makes the person under
            18 years old.
            :raises ValidationError: If the person is under 18."""
        if self.date_of_birth:
            if (fields.date.today().year - self.date_of_birth.year) < 18:
                raise ValidationError(_('Veuillez fournir une date de naissance valide'))
