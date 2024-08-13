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


class UniversityAcademicYear(models.Model):
    """For managing university academic year"""
    _name = 'university.academic.year'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Academic Year"

    name = fields.Char(string="Nom", help="Nom de l'année académique")
    start_date = fields.Date(string="Date de début", required=True,
                             help="Entrez la date de début de l'année académique")
    end_date = fields.Date(string="Date de fin", required=True,
                           help="Entrez la date de fin de l'année académique")
    is_active = fields.Boolean(
        'Actif', default=True,
        help="Si décoché, cela vous permettra de cacher l'année académique "
             "sans la supprimer.")
