from odoo import models, fields, api


class MyPartner(models.Model):
    _inherit = 'res.partner'

    iti_instructor = fields.Boolean('ITI Instructor', default=False)

    courses_ids = fields.One2many('iti.course', 'iti_instructor_id', string='Courses', readonly=True)
