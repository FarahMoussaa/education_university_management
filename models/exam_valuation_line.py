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
from odoo.exceptions import UserError


class ExamValuationLine(models.Model):
    """Used to record the students pass mark details while valuing the exam"""
    _name = 'exam.valuation.line'
    _description = 'Exam Valuation Line'
    student_id = fields.Many2one('university.student',
                                string='Étudiants',
                                help="Étudiants de la promotion")
    mark_scored = fields.Float(string='Note',
                            help="Note obtenue par l'étudiant")
    is_pass = fields.Boolean(string='Réussi/Échoué',
                            help="Activez si l'étudiant a réussi l'examen",
                            default=False)
    valuation_id = fields.Many2one('exam.valuation',
                                help="Relation avec le modèle de validation d'examen",
                                string='ID de validation')

  

    @api.onchange('mark_scored', 'is_pass')
    def _onchange_mark_scored(self):
        """to determine whether the scored mark exceeds the subject's
          maximum mark and determine pass/fail depending on the scored mark."""
        if self.mark_scored > self.valuation_id.mark:
            raise UserError(_('Le score obtenu doit être inférieur à la note maximale.'))
        self.is_pass = True if \
            self.mark_scored >= self.valuation_id.pass_mark else False