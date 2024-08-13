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


class UniversityBatch(models.Model):
    """For managing batches of every department in the university"""
    _name = 'university.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Batches"

    @api.model
    def create(self, vals):
        """Return the name as a str of semester + academic year"""
        semester_id = self.env['university.semester'].browse(
            vals['semester_id'])
        academic_year_id = self.env['university.academic.year'].browse(
            vals['academic_year_id'])
        name = str(semester_id.name + ' - ' + academic_year_id.name)
        vals['name'] = name
        return super(UniversityBatch, self).create(vals)

    name = fields.Char(string="Nom", help="Nom de la promotion", readonly=True)
    semester_id = fields.Many2one('university.semester',
                                  string="Semestre", required=True,
                                  help="Sélectionnez le semestre")
    department_id = fields.Many2one(related='semester_id.department_id',
                                    string="Département",
                                    help="À quel département cette promotion appartient-elle")
    academic_year_id = fields.Many2one('university.academic.year',
                                       string="Année Académique", required=True,
                                       help="Sélectionnez l'année académique")
    batch_strength = fields.Integer(string='Effectif de la Promotion',
                                    help="Effectif total de la promotion")
    faculty_id = fields.Many2one('university.faculty',
                                 string='Faculté', help="Tuteur/Enseignant de la promotion")
    batch_student_ids = fields.One2many('university.student',
                                        'batch_id',
                                        string="Étudiants",
                                        help="Étudiants de cette promotion")
