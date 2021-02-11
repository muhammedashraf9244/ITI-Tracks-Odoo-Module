from odoo import models,fields

class ItITrack(models.Model):
    _name = 'iti.track'
    name=fields.Char()
    capacity=fields.Integer()
    is_open=fields.Boolean()
    student_ids=fields.One2many('iti.student','track_id')
    courses_ids = fields.One2many('course.track.line','track_id')

class ItiCourse(models.Model):
    _name = 'iti.course'
    name=fields.Char()
    total_grade=fields.Integer()
    tracks_ids = fields.One2many('course.track.line','course_id')



class ItiCoursesTracks(models.Model):
    _name = "course.track.line"
    course_id = fields.Many2one('iti.course')
    track_id = fields.Many2one('iti.track')
    hours = fields.Integer(string='Hours Of Course',required=True)