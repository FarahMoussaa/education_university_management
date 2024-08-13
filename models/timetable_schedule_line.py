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


class TimeTableScheduleLine(models.Model):
    """ Manages the schedule for subjects and faculty while
        creating timetable"""
    _name = 'timetable.schedule.line'
    _description = 'Timetable Schedule'
    _rec_name = 'period_id'

    period_id = fields.Many2one('timetable.period',
                                string="Période", required=True,
                                help="Sélectionnez la période")
    faculty_id = fields.Many2one('university.faculty',
                                 string='Faculté', required=True,
                                 help="Définir la faculté qui prend en charge ")
    time_from = fields.Float(string='De', related='period_id.time_from',
                             readonly=False,
                             help="Heure de début et de fin de la période.")
    time_till = fields.Float(string="Jusqu'à", related='period_id.time_to',
                             readonly=False,
                             help="Heure de début et de fin de la période.")
    subject = fields.Many2one('university.subject',
                              string='Matières', required=True,
                              help="Sélectionner la matière pour programmer l'emploi du temps")
    week_day = fields.Selection([
        ('0', 'Lundi'),
        ('1', 'Mardi'),
        ('2', 'Mercredi'),
        ('3', 'Jeudi'),
        ('4', 'Vendredi'),
        ('5', 'Samedi'),
        ('6', 'Dimanche'),
    ], string='Jour de la semaine', required=True, help="Sélectionner le jour de la semaine pour programmer la période")
    timetable_id = fields.Many2one('university.timetable',
                                   required=True, string="Emploi du temps",
                                   help="Relation avec university.timetable")
    batch_id = fields.Many2one('university.batch', string='Promotion',
                               help="Promotion")

    @api.model
    def create(self, vals):
        """ This method overrides the create method to automatically store
            :param vals (dict): Dictionary containing the field values for the
                                new timetable schedule line.
            :returns class:`timetable.schedule.line`The created timetable
                            schedule line record. """
        res = super(TimeTableScheduleLine, self).create(vals)
        res.batch_id = res.timetable_id.batch_id.id
        return res
