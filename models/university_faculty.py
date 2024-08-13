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
from odoo import fields, models


class UniversityFaculty(models.Model):
    """For managing faculties of university"""
    _name = 'university.faculty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Faculty records"

    name = fields.Char(string='Nom', required=True,
                       help="Entrez le Nom")
    last_name = fields.Char(string='Prènom', help="Entrez le prénom")
    image = fields.Binary(string="Image", attachment=True,
                      help="Image de la faculté")
    date_of_birth = fields.Date(string="Date de naissance", required=True,
                            help="Entrez la date de naissance")
    email = fields.Char(string="Email", required=True,
                    help="Entrez l'email pour des raisons de contact")
    phone = fields.Char(string="Téléphone",
                    help="Entrez le téléphone pour des raisons de contact")
    mobile = fields.Char(string="Mobile", required=True,
                     help="Entrez le mobile pour des raisons de contact")
    guardian_id = fields.Char(string="Tuteur", help="Votre tuteur est")
    father_name = fields.Char(string="Père", help="Le nom de votre père est")
    mother_name = fields.Char(string="Mère", help="Le nom de votre mère est")
    degree_id = fields.Many2one('hr.recruitment.degree',
                            string="Diplôme",
                            help="Sélectionnez votre diplôme le plus élevé")
    subject_line_ids = fields.Many2many('university.subject',
                                    string='Lignes de sujet',
                                    help="Sujets de la faculté")
    employee_id = fields.Many2one('hr.employee',
                              string="Employé lié",
                              help="Employé lié à la faculté")
    gender = fields.Selection(
                                [('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')],
                                string='Genre', required=True, default='male',
                                help="Genre de la faculté",
                                track_visibility='onchange')
    blood_group = fields.Selection(
                                [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
                                ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')],
                                string='Groupe sanguin', required=True, default='a+',
                                help="Groupe sanguin de la faculté", track_visibility='onchange')

    def action_create_employee(self):
        """Creating the employee for the faculty"""
        for rec in self:
            emp_id = self.env['hr.employee'].create({
                'name': rec.name + ' ' + rec.last_name,
                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                'image_1920': rec.image,
                'work_phone': rec.phone,
                'work_email': rec.email,
            })
            rec.employee_id = emp_id.id
