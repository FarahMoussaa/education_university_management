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
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class UniversityAttendance(models.Model):
    """For managing student daily attendance details"""
    _name = 'university.attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Student attendance"

    name = fields.Char(string="Nom", default="New",
                       help="Nom de la présence")
    batch_id = fields.Many2one('university.batch', string="Promotion",
                               required=True,
                               help="Sélectionnez la promotion pour la présence")
    faculty_id = fields.Many2one(related='batch_id.faculty_id',
                                 string="Faculté",
                                 help="Faculté responsable de la promotion")
    date = fields.Date(string="Date", default=fields.Date.today, required=True,
                       help="Sélectionnez la date de la présence")
    attendance_line_ids = fields.One2many('university.attendance.line',
                                          'attendance_id',
                                          string='Ligne de présence',
                                          help="Liste des présences des étudiant")
    state = fields.Selection([('draft', 'Brouillon'), ('done', 'Terminé')],
                             default='draft', help="Statut de la présence")
    is_all_marked_morning = fields.Boolean(
        string='Tous les étudiants sont présents le matin',
        help="Est-ce que tous les étudiants sont présents le matin")
    is_all_marked_afternoon = fields.Boolean(
       string="Tous les étudiants sont présents l'après-midi",
        help="Est-ce que tous les étudiants sont présents l'après-midi")
    is_attendance_created = fields.Boolean(string='Présence créée',
                                           help="La présence est-elle créée ou non")

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        """ Method to clear the attendance line if the batch is changed """
        if self.batch_id:
            self.is_attendance_created = False
            self.attendance_line_ids = False

    def action_create_attendance_line(self):
        """Action to create attendance line with students in the batch"""
        if self.search_count(
                [('batch_id', '=', self.batch_id.id), ('date', '=', self.date),
                 ('state', '=', 'done')]) == 1:
            raise ValidationError(
                _('La présence pour cette promotion à cette date existe déjà.'))
        self.name = str(self.date)
        if len(self.batch_id.batch_student_ids) < 1:
            raise UserError(_("Il n'y a aucun étudiant dans cette promotion"))
        for student in self.batch_id.batch_student_ids:
            self.env['university.attendance.line'].create(
                {'name': self.name,
                 'attendance_id': self.id,
                 'student_id': student.id,
                 'batch_id': self.batch_id.id,
                 'date': self.date, })
        self.is_attendance_created = True

    def action_mark_all_present_morning(self):
        """Action to mark all marked presents of students in the morning"""
        for records in self.attendance_line_ids:
            records.is_present_morning = True
        self.is_all_marked_morning = True

    def action_un_mark_all_present_morning(self):
        """Action to unmark all marked presents of students in the morning"""
        for records in self.attendance_line_ids:
            records.is_present_morning = False
        self.is_all_marked_morning = False

    def action_mark_all_present_afternoon(self):
        """Action to mark all marked presents of students in the afternoon"""
        for records in self.attendance_line_ids:
            records.is_present_afternoon = True
        self.is_all_marked_afternoon = True

    def action_un_mark_all_present_afternoon(self):
        """Action to unmark all marked presents of students in the afternoon"""
        for records in self.attendance_line_ids:
            records.is_present_afternoon = False
        self.is_all_marked_afternoon = False

    def action_attendance_done(self):
        """To compute absent of student is half/full day and
                        make the attendance to done stage"""
        for records in self.attendance_line_ids:
            if not records.is_present_morning and \
                    not records.is_present_afternoon:
                records.full_day_absent = 1
            elif not records.is_present_morning:
                records.half_day_absent = 1
            elif not records.is_present_afternoon:
                records.half_day_absent = 1
        self.state = 'done'
