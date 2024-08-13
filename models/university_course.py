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


class UniversityCourse(models.Model):
    """Used to managing the courses of university"""
    _name = 'university.course'
    _description = "University Courses"

    name = fields.Char(string="Nom", required=True, help="Nom du cours")
   
    category = fields.Selection(
        [('ug', "En cours d'obtention du diplôme"), ('pg', "Après l'obtention du diplôme"),
         ('diploma', 'Diploma')], string="Catégorie de cours", required=True,
        help="À quelle catégorie appartient le cours")
    no_semester = fields.Integer(string="N° de semestre",
                                 help="Nombre de semestres dans chaque cours")





