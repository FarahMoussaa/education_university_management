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
from odoo import api, fields, models


class UniversitySyllabus(models.Model):
    """Manages the syllabus of department"""
    _name = 'university.syllabus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Syllabus"

    @api.model
    def create(self, vals):
        """ This method overrides the create method to generate the name for the
            syllabus based on the department and subject.
           :param vals (dict): Dictionary containing the field values for the
                              new university syllabus record.
           :returns class:`university.syllabus` The created university
                                                    syllabus record."""
        """Return the name as a str of course code + subject code"""
        semester_id = self.env['university.semester'].browse(
            vals['semester_id'])
        subject_id = self.env['university.subject'].browse(
            vals['subject_id'])
        name = str(semester_id.name) + '/' + str(
            subject_id.code) + '-Syllabus'
        vals['name'] = name
        return super(UniversitySyllabus, self).create(vals)

    name = fields.Char(string="Nom", help="Nom du programme", readonly=True)
    subject_id = fields.Many2one('university.subject',
                                 required=True, string="Matières",
                                 help="Sélectionner un sujet pour le programme")
    total_hrs = fields.Float(string="Heures totales",
                             help="Temps pour terminer les matières")
    description = fields.Text(string='Détails du module',
                              help="Description des modules")
    subject_code = fields.Char(related='subject_id.code', string="Code",
                               help="Code sujet du sujet sélectionné")
    subject_weightage = fields.Float(related='subject_id.weightage',
                                     help="Points du sujet")
    semester_id = fields.Many2one('university.semester',
                                  string="Semestre", required=True,
                                  help="Sélectionner un semestre pour le programme")
    department_id = fields.Many2one(related='semester_id.department_id',
                                    string="Département",
                                    help="Sélectionner le département pour le programme")
