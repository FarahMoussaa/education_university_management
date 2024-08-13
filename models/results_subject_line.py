# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana Jabin MP  (odoo@cybrosys.com)
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


class ResultsSubjectLine(models.Model):
    """Used to manage subject details of student exam result"""
    _name = 'results.subject.line'
    _description = 'Results Subject Line'

    name = fields.Char(string='Nom', help="Nom du résultat")
    subject_id = fields.Many2one('university.subject',
                                 string='Matière',
                                 help="Matières de l'examen")
    max_mark = fields.Float(string='Note Maximale', help="Note maximale de la matière")
    pass_mark = fields.Float(string='Note de Passage',
                             help="Note de passage de la matière")
    mark_scored = fields.Float(string='Note Obtenue',
                               help="Notes obtenues par les étudiants dans les matières")
    is_pass = fields.Boolean(string='Réussite/Échec',
                             help="Relation avec le modèle des résultats")
    result_id = fields.Many2one('exam.result', string='ID du Résultat',
                                help="Relation avec le modèle des résultats")
