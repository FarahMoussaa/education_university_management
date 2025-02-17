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
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class UniversityTimeTable(models.Model):
    """Manages the timetable of every batch"""
    _name = 'university.timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Timetable'

    name = fields.Char(string="Nom", compute="_compute_name",
                       help="Nom de l'horaire")
    batch_id = fields.Many2one('university.batch', string='Promotion',
                               help="Lot d'horaires",
                               required=True)
    academic_year_id = fields.Many2one(related="batch_id.academic_year_id",
                                       help="Année académique de la promotion",
                                       string='Année académique')
    mon_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Ligne programmée du lundi",
                                        domain=[('week_day', '=', '0')])
    tue_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Ligne prévue du mardi ",
                                        domain=[('week_day', '=', '1')])
    wed_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Ligne programmée du mercredi",
                                        domain=[('week_day', '=', '2')])
    thur_timetable_ids = fields.One2many('timetable.schedule.line',
                                         'timetable_id',
                                         help="Ligne programmée du jeudi",
                                         domain=[('week_day', '=', '3')])
    fri_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Ligne prévue du vendredi",
                                        domain=[('week_day', '=', '4')])
    sat_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Ligne programmée du samedi",
                                        domain=[('week_day', '=', '5')])
    company_id = fields.Many2one(
        'res.company', string='Entreprise', help="Entreprise",
        default=lambda self: self.env.company)

    def _compute_name(self):
        """generate name for the timetable records"""
        for rec in self:
            rec.name = False
            if rec.batch_id and rec.academic_year_id:
                rec.name = "/".join([rec.batch_id.name, "Schedule"])

    @api.constrains('batch_id')
    def _check_batch(self):
        """ This method ensures that only one timetable can be scheduled for a
            specific Batch.

            :raises: ValidationError if more than one timetable is already
                    scheduled for the Batch."""
        batches = self.search_count([('batch_id', '=', self.batch_id.id)])
        if batches > 1:
            raise ValidationError(_('Un emploi du temps est déjà prévu pour '
                                    'cette promotion'))
