from odoo import models,fields,api

class ItITrack(models.Model):
    _name = 'iti.track'
    name=fields.Char()
    capacity=fields.Integer()
    is_open=fields.Boolean()
    student_ids=fields.One2many('iti.student','track_id')
