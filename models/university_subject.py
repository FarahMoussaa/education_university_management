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


class UniversitySubject(models.Model):
    """For managing subjects of every courses"""
    _name = 'university.subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Subjects"

    name = fields.Char(string="Matière", help="Nom de la matière")
    is_language = fields.Boolean(string="Langue",
                                 help="Cochez si ce matière est une langue")
    is_lab = fields.Boolean(string="Lab", help="Cochez si ce sujet est un Lab")
    code = fields.Char(string="Code", help="Entrez le code matière")
    type = fields.Selection(
        [('compulsory', 'Obligatoire'), ('elective', 'Électif')],
        string='Type', default="compulsory",
        help="Choisissez le type de matière")
    weightage = fields.Float(string='Poids', default=1.0,
                             help="Entrez le poids de cette matière")
    description = fields.Text(string='Description',
                              help=" Description du matière")
