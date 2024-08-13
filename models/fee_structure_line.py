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


class FeeStructureLines(models.Model):
    _name = 'fee.structure.line'
    _description = "Fee Structure lines"

    fee_structure_id = fields.Many2one('fee.structure',
                                    help="Relation avec la structure des frais",
                                    string='Structure des frais',
                                    ondelete='cascade', index=True)
    category_id = fields.Many2one(related='fee_structure_id.category_id',
                                string="Catégorie",
                                help="Catégorie des frais de la structure")
    fee_type_id = fields.Many2one('fee.type', string='Frais',
                                required=True, help="Sélectionnez les types de frais")
    currency_id = fields.Many2one('res.currency', string="Monnaie",
                                default=lambda
                                    self: self.env.user.company_id.currency_id.id,
                                help="Monnaie de l'entreprise actuelle")
    fee_amount = fields.Float('Montant', required=True,
                            help="Montant de chaque type de frais",
                            related='fee_type_id.lst_price')
    payment_type = fields.Selection(string='Type de paiement',
                                    help="Type de paiement du type de frais",
                                    related="fee_type_id.payment_type")
    fee_description = fields.Text('Description', help="Description du type de frais",
                                related='fee_type_id.description_sale')
