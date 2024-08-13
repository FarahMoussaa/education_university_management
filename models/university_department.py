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


class UniversityDepartment(models.Model):
    """Used to manage department of every courses"""
    _name = 'university.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Department"

    name = fields.Char(string="Nom", help="Nom du cours")
    code = fields.Char(string="Code", help="Code du cours", required=True)
    course_id = fields.Many2one('university.course',
                                string="Cours", required=True,
                                help="À quel cours appartient le département")
    semester_ids = fields.One2many('university.semester',
                                   'department_id',
                                   string="Semestre", required=1,
                                   help="Liste des semestres pour chaque cours")
