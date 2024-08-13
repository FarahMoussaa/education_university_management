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
from odoo import fields, models


class ExamSubjectLine(models.Model):
    """For managing the subjects in the exam"""
    _name = 'exam.subject.line'
    _description = 'Subject Line of Exam'

    subject_id = fields.Many2one('university.subject',
                                 string='Matière', required=True,
                                 help="Sélectionnez les matières de l'examen")
    date = fields.Date(string='Date', required=True,
                   help="Sélectionnez la date de la matière")
    time_from = fields.Float(string='Heure de début', required=True,
                            help="Entrez l'heure de début de la matière")
    time_to = fields.Float(string='Heure de fin', required=True,
                        help="Entrez l'heure de fin de la matière")
    mark = fields.Integer(string='Note', help="Entrez la note pour la matière")
    exam_id = fields.Many2one('university.exam', string='Examen',
                            help="Relation avec le modèle d'examen")
    company_id = fields.Many2one('res.company', string='Entreprise',
                                help="Entreprise de l'examen",
                                default=lambda self: self.env.company)