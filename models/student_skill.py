from odoo import models,fields


class StudentSkill(models.Model):
    _name = 'student.skill'

    name= fields.Char()
