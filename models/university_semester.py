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


class UniversitySemester(models.Model):
    """Used to manage the semester of department"""
    _name = 'university.semester'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Semester"

    @api.model
    def create(self, vals):
        """ This method overrides the create method to generate the name for
            the semester based on the department code and semester number.

            :param vals (dict): Dictionary containing the field values for the
                                new university semester record.
            :returns class:`~university.semester`: The created university
                            semester record."""
        department_id = self.env['university.department'].browse(
            vals['department_id'])
        name = str(department_id.code) + '/Sem ' + str(vals['semester_no'])
        vals['name'] = name
        return super(UniversitySemester, self).create(vals)

    name = fields.Char(string="Nom", help="Nom du semestre",
                       readonly=True)
    semester_no = fields.Integer(string="Semestre", help="Numéro de semestre",
                                 required=True)
    department_id = fields.Many2one('university.department',
                                    string="Département",
                                    required=True,
                                    help="Dans quel département le semestre "
                                         "appartient à")
    syllabus_ids = fields.One2many('university.syllabus',
                                   'semester_id',
                                   help="Programme du semestre",
                                   string="Programme")
