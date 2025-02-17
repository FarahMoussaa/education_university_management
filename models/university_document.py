# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana jabin MP (odoo@cybrosys.com)
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


class UniversityDocuments(models.Model):
    """For managing the student document verification details"""
    _name = 'university.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Students Documents"

    name = fields.Char(string="Reference No.", copy=False,
                       help="Sequence of the document",
                       default=lambda self: _('New'))
    document_type_id = fields.Many2one('university.document.type',
                                       string="Document Type", required=True,
                                       help="Choose the type of document")
    application_ref_id = fields.Many2one('university.application',
                                         string="Demande Réf.",
                                         help="référence d'application du document " )
    description = fields.Text(string='Description',
                              help="Entrez une description du document")
    verified_date = fields.Date(string="Date de vérification",
                                help="Date à laquelle la vérification est effectuée")
    verified_by_id = fields.Many2one('res.users',
                                     string='Vérifié par',
                                     help="Document Utilisateur vérifié")
    responsible_verified_id = fields.Many2one('hr.employee',
                                              string="Responsable",
                                              help="Personne responsable de "
                                                   "vérification")
    attachment_ids = fields.Many2many(
        'ir.attachment', 'university_attach_rel',
        'doc_id', 'doc_attach_id',
        string="Pièce jointe", required=True,
        help='Vous pouvez joindre la copie de votre document',
        copy=False)
    state = fields.Selection(
        [('draft', 'Brouillon'), ('correction', 'Correction'),
         ('done', 'Terminé')], string='Statut', required=True, default='draft',
        help="Statut du document", track_visibility='onchange')

    @api.model
    def create(self, vals):
        """ This method overrides the create method to assign a sequence to
            newly created records.
           :param vals (dict): Dictionary containing the field values
                               for the new university document record.
           :returns class:`~university.documents`: The created university
                                                   document record. """
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'university.document') or _('New')
        res = super(UniversityDocuments, self).create(vals)
        return res

    def action_verify_document(self):
        """ This method updates the state of the university document to 'done'
            if the documents are deemed perfect."""
        for rec in self:
            rec.write({
                'verified_by_id': self.env.uid,
                'verified_date': fields.Datetime.now().strftime("%Y-%m-%d"),
                'state': 'done'
            })

    def action_need_correction(self):
        """ This method updates the state of the university document to
            'correction' if the documents are deemed not perfect and
            require correction."""
        for rec in self:
            rec.write({
                'state': 'correction'
            })
