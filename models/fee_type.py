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


class FeeTypes(models.Model):
    """For managing payment method or type of student fees"""
    _name = 'fee.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'product.product': 'product_id'}
    _description = 'University fees'

    payment_type = fields.Selection([
        ('onetime', 'Unique'),
        ('permonth', 'Par mois'),
        ('peryear', 'Par an'),
        ('sixmonth', '6 mois'),
        ('threemonth', '3 mois')],
        string='Type de paiement', default='permonth',
        help='Le type de paiement décrit combien un paiement est effectif')
    category_id = fields.Many2one('fee.category', string='Catégorie',
                                  help="Catégorie des types de frais",
                                  required=True)
    currency_id = fields.Many2one('res.currency', string="Monnaie",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id,
                                  help="Monnaie de l'entreprise actuelle")
    product_id = fields.Many2one('product.product',
                                 string='Produit', required=True,
                                 ondelete='cascade')
