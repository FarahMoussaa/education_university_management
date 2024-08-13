# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:Jumana Jabin MP (odoo@cybrosys.com)
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


class UniversityAttendanceLine(models.Model):
    """For recording if the student is present during the day or not."""
    _name = 'university.attendance.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Attendance Lines'

    name = fields.Char(string='Nom', help="Nom de la présence")
    attendance_id = fields.Many2one('university.attendance',
                                    string='ID de Présence',
                                    help="Champ de relation avec le module de présence")
    student_id = fields.Many2one('university.student',
                                 string='Étudiant',
                                 help="Étudiants du promotion")
    is_present_morning = fields.Boolean(string='Matin',
                                        help="L'étudiant est-il présent le matin")
    is_present_afternoon = fields.Boolean(string='Après-midi',
                                          help="L'étudiant est-il présent l'après-midi")
    full_day_absent = fields.Integer(string='Journée Complète',
                                     help="L'étudiant est-il absent toute la journée ou non")
    half_day_absent = fields.Integer(string='Demi-Journée',
                                     help="L'étudiant est-il absent une demi-journée ou non")
    batch_id = fields.Many2one('university.batch', string="Promotion",
                               required=True,
                                help="Sélectionner la promotion pour la présence")
    date = fields.Date(string='Date', required=True, help="Date de la présence")
