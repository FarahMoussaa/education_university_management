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


class UniversityExam(models.Model):
    """Used to manage student exams of every semester"""
    _name = 'university.exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Student Exam management"

    name = fields.Char(string='Nom', default='New', help="Nom de l'examen")
    batch_id = fields.Many2one('university.batch', string='promotion',
                               help="Quel examen de la promotion est")
    exam_type_id = fields.Many2one('university.exam.type',
                                   string='Type', help="Type d'examen",
                                   required=True)
    start_date = fields.Date(string='Date de début', required=True,
                             help="Entrez la date de début de l'examen")
    end_date = fields.Date(string='Date de fin', required=True,
                           help="Entrez la date de fin de l'examen")
    subject_line_ids = fields.One2many('exam.subject.line',
                                       'exam_id', string='matière',
                                       help="Matières de l'examen")
    state = fields.Selection(
        [('draft', 'Brouillon'),
         ('ongoing', 'En cours'),
         ('close', 'Fermé'),
         ('cancel', 'Annulé')],
        default='draft', help="Statut de l'examen")
    academic_year_id = fields.Many2one(related='batch_id.academic_year_id',
                                       string='Année académique',
                                       help="Année académique de la promotion")
    company_id = fields.Many2one(
        'res.company', string='Entreprise', help="Entreprise de l'examen",
        default=lambda self: self.env.company)

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        """ This constraint method validates that the start date of the exam is
             earlier than the end date.
            :raises ValidationError: If the start date is greater than the
                                     end date"""
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError(
                    _("La date de début doit être antérieure à la date de fin"))

    def action_close_exam(self):
        """ This method sets the state of the exam to 'close',
            indicating that the exam has been closed."""
        self.state = 'close'

    def action_cancel_exam(self):
        """ This method sets the state of the exam to 'cancel',
            indicating that the exam has been canceled."""
        self.state = 'cancel'

    def action_confirm_exam(self):
        """ This method confirms the exam and checks if at least
            one subject is added to the exam.
            :raises UserError: If no subjects are added to the exam."""
        if len(self.subject_line_ids) < 1:
            UserError(_('Please Add Subjects'))
        self.name = str(self.exam_type_id.name) + '/' + str(self.start_date)[
                                                        0:10] + ' (' + str(
            self.batch_id.name) + ')'
        self.state = 'ongoing'
