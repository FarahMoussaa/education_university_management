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
from odoo import api, fields, models


class FeeStructure(models.Model):
    """Managing the fee structure for university students"""
    _name = 'fee.structure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Fees structure of university"

    name = fields.Char('Nom', required=True,
                   help="Entrez le nom de la structure des frais")
    currency_id = fields.Many2one('res.currency', string="Monnaie",
                              default=lambda
                                  self: self.env.user.company_id.currency_id.id,
                                help="Monnaie de l'entreprise actuelle")
    structure_line_ids = fields.One2many('fee.structure.line',
                                        'fee_structure_id',
                                        string='Types de frais',
                                        help="Lignes de la structure des frais")
    description = fields.Text(string="Informations supplémentaires",
                            help="Toute information supplémentaire à propos de")
    academic_year_id = fields.Many2one('university.academic.year',
                                    help="Choisissez l'année académique",
                                    string='Année académique', required=True)
    amount_total = fields.Float(string="Montant", currency_field='currency_id',
                                help="Montant total des lignes",
                                required=True, compute='_compute_total')
    category_id = fields.Many2one('fee.category', string='Catégorie',
                                help="Sélectionnez la catégorie pour la structure",
                                required=True)

    @api.depends('structure_line_ids.fee_amount')
    def _compute_total(self):
        """Method for computing total amount of the structure lines"""
        self.amount_total = sum(
            line.fee_amount for line in self.structure_line_ids)
