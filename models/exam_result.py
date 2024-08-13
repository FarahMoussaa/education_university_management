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


class ExamResult(models.Model):
    """Creating a model for storing students exam result."""
    _name = 'exam.result'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Result"

    name = fields.Char(string='Nom', help="Nom du résultat de l'examen")
    exam_id = fields.Many2one('university.exam', string='Examen',
                              help="À quel examen ce résultat appartient-il")
    batch_id = fields.Many2one('university.batch', string='Promotion',
                               help="À quelle promotion ce résultat appartient-il")
    student_id = fields.Many2one('university.student',
                                 string='Étudiant', help="Résultat de l'étudiant")
    subject_line_ids = fields.One2many('results.subject.line',
                                       'result_id',
                                        help="Résultat de chaque matière dans l'examen",
                                    string='Matières')
    academic_year_id = fields.Many2one(related='batch_id.academic_year_id',
                                         help="Année académique de la promotion",
                                   string='Année académique')
    company_id = fields.Many2one(
        'res.company', string='Entreprise', help="Entreprise pour laquelle le résultat est",
        default=lambda self: self.env.company)
    total_pass_mark = fields.Float(string='Note totale de passage', store=True,
                                help="Note totale pour réussir l'examen",
                                readonly=True, compute='_total_marks_all')
    total_max_mark = fields.Float(string='Note maximale totale', store=True,
                                help="Note maximale de l'examen",
                                readonly=True,
                                compute='_compute_total_marks')
    total_mark_scored = fields.Float(string='Total des notes obtenues', store=True,
                                    help="Total des notes obtenues par l'étudiant",
                                    readonly=True,
                                    compute='_compute_total_marks')
    is_overall_pass = fields.Boolean(string='Réussi/Échoué global', store=True,
                                    help="Ratio global de réussite ou d'échec",
                                    readonly=True,
                                    compute='_compute_total_marks')

    @api.depends('subject_line_ids.mark_scored')
    def _compute_total_marks(self):
        """This method is for computing total mark scored and overall
                    pass details"""
        for results in self:
            total_pass_mark = 0
            total_max_mark = 0
            total_mark_scored = 0
            is_overall_pass = True
            for subjects in results.subject_line_ids:
                total_pass_mark += subjects.pass_mark
                total_max_mark += subjects.max_mark
                total_mark_scored += subjects.mark_scored
                if not subjects.is_pass:
                    is_overall_pass = False
            results.total_pass_mark = total_pass_mark
            results.total_max_mark = total_max_mark
            results.total_mark_scored = total_mark_scored
            results.is_overall_pass = is_overall_pass
