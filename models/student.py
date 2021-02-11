from odoo import fields,models,api

class ItiStudent(models.Model):
    _name='iti.student'
    name=fields.Char(required=True)
    salary=fields.Float()
    birthday=fields.Date()
    address=fields.Text()
    gender=fields.Selection([('m','Male'),('f','Female')])
    accepted=fields.Boolean()
    image=fields.Binary()  #image=fields.Image()
    cv=fields.Html()
    track_id=fields.Many2one('iti.track')
    track_capacity=fields.Integer(related='track_id.capacity')
    skills_ids=fields.Many2many('student.skill')
    gradestudent_ids=fields.One2many('iti.course.line','student_id')

    @api.onchange("gender")
    def _change_salary(self):
        domain = {'track_id': []}
        if self.gender=='m':
            doamin={'track_id':['is_open','=',False]}
            self.salary=1000
            return {}
        elif self.gender=='f':
            self.salary=500
        return {
            'warning': {
                'title': "Change Salary",
                'message': 'change salary if change geneder',
            },
            'domain':domain
        }



class ItiCourseGrade(models.Model):
    _name = 'iti.course.line'
    student_id=fields.Many2one('iti.student')
    course_id=fields.Many2one('iti.course')
    grade=fields.Selection([('e','Excelent'),('vg','VeryGood'),('g','Good'),
                            ('p','Passing')])

    