# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana Jabin MP(odoo@cybrosys.com)
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


class FeeCategory(models.Model):
    """For managing the categories for university fees"""
    _name = 'fee.category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Categories of university fees"

    name = fields.Char('Name', required=True,
                       help="Créer une catégorie de frais adaptée à l'institution."
                            ' Comme les institutions, les auberges, les transports, '
                            'Arts et sports, etc')
    journal_id = fields.Many2one('account.journal',
                                 domain="[('is_fee', '=', 'True')]",
                                 required=True, string='Journal',
                                 help="Mise en place d'un journal uniquel "
                                      'pour chaque catégorie, aide à distinguer'
                                      'écritures de compte de chaque catégorie ')
