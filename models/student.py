from odoo import fields,models,api

class ItiStudent(models.Model):
    _name='iti.student'
    name=fields.Char(required=True)
    salary=fields.Float(readonly=True)
    birthday=fields.Date()
    address=fields.Text()
    gender=fields.Selection([('m','Male'),('f','Female')])
    accepted=fields.Boolean()
    image=fields.Binary()
    cv=fields.Html()
    track_id=fields.Many2one('iti.track')
    track_capacity=fields.Integer(related='track_id.capacity')
    skills_ids=fields.Many2many('student.skill')
    gradestudent_ids=fields.One2many('iti.course.line','student_id')



class ItiCourse(models.Model):
    _name = 'iti.course'

    name=fields.Char()
    total_grade=fields.Integer()
    gradecourse_ids=fields.One2many('iti.course.line','course_id')

class ItiCourseGrade(models.Model):
    _name = 'iti.course.line'
    student_id=fields.Many2one('iti.student')
    course_id=fields.Many2one('iti.course')
    grade=fields.Selection([('e','Excelent'),('vg','VeryGood'),('g','Good'),
                            ('p','Passing')])

    