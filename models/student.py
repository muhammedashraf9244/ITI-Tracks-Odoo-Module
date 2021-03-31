from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime


class ItiStudent(models.Model):
    _name = 'iti.student'
    name = fields.Char(required=True)
    email = fields.Char()
    salary = fields.Float()
    tax = fields.Float(compute="calc_salary")
    net_salary = fields.Float(compute="calc_salary")
    birthday = fields.Date()
    age = fields.Integer(compute="get_age", store=True)
    address = fields.Text()
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')])
    accepted = fields.Boolean()
    image = fields.Binary()  # image=fields.Image()
    cv = fields.Html()
    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(related='track_id.capacity')
    skills_ids = fields.Many2many('student.skill')
    grade_student_ids = fields.One2many('iti.course.line', 'student_id')
    state = fields.Selection([('applied', 'Applied')
                                 , ('first', 'First Interview')
                                 , ('second', 'Second Interview')
                                 , ('passed', 'Passed')
                                 , ('rejected', 'Rejected')], default='applied')

    responsible_id = fields.Many2one('res.users', ondelete='set null', string='Responsible', index=True,
                                     default=lambda self: self.env.uid)

    def _get_report_filename(self):
        return "Students Report" if (len(self) > 1) else f"{self.name} Report".title()

    # compute function
    @api.depends("salary")
    def calc_salary(self):
        # self.ensure_one()  # raise error if compute for many record
        for record in self:
            record.tax = record.salary * .50
            record.net_salary = record.salary - record.tax

    @api.depends("birthday")
    def get_age(self):
        for record in self:
            if record.birthday:
                # print(str(record.birthday))
                # convert date type to datetime
                birth_date_time = datetime.strptime(str(record.birthday), "%Y-%m-%d")
                # print(birth_date_time)
                # calc differance between two dates
                record.age = abs((birth_date_time - datetime.now()).days) // 365

    # sql constraints is useful for small logic
    _sql_constraints = [
        ("Unique Name", "UNIQUE(name)", "this name is already exists"),
        ("Unique Email", "UNIQUE(email)", "this email is already exists"),
    ]

    # function of status
    def change_state_first(self):
        self.state = self.state and 'first'

    def change_state_second(self):
        self.state = self.state and 'second'

    def passed_state(self):
        self.state = self.state and 'passed'

    def reject_state(self):
        self.state = self.state and 'rejected'

    def back_to_appy(self):
        self.state = 'applied' if self.state in ['passed', 'rejected'] else ''

    @api.model
    def create(self, vals_list):
        name_split = vals_list['name'].split()  # split name ["Mohammed","Ashraf"]
        vals_list['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_email = self.search([('email', '=', vals_list['email'])])
        if search_email:
            raise UserError('This email is exits ')
        # browe_object=self.browse(ids=[5,9])
        # print(browe_object)
        # Solve if track is closed
        """
        check_track = self.env['iti.track'].search([('id','=',vals_list['track_id']),('is_open','!=',True)])
        if check_track:
            raise UserError(f'The Track {check_track.name} is not allowed students')
        """
        track = self.env['iti.track'].browse(vals_list['track_id'])
        if not track.is_open:
            raise UserError(f'The Track {track.name} is not allowed students')
        return super().create(vals_list)

    """
    in #Odoo 13 both the http://api.one and the api.multi will be removed! By default
    every function will be a recordset and you don't have to provide these decorators (anymore)
    """

    # In write function not all fields has data so use 'field' in vals
    def write(self, vals_list):
        if 'name' in vals_list:
            name_split = vals_list['name'].split()  # split name ["Mohammed","Ashraf"]
            vals_list['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().write(vals_list)

    def unlink(self):
        for student in self:
            if student.state in ['passed', 'rejected']:
                raise UserError('Not allowed delete student in state passed or rejected')
        super().unlink()

    @api.constrains("salary")
    def _check_name(self):
        for record in self:
            if record.salary > 1000:
                raise UserError('Salary bigger than 1000')

    @api.constrains("track_id")
    def _check_capcity_track(self):
        for record in self:
            count_track = len(record.track_id.student_ids)
            # print("Capcity ",self.track_id.student_ids)
            if count_track > record.track_capacity:
                raise UserError(f'This {record.track_id.name} track is full sorry not opend now')

    @api.onchange("gender")
    def _change_salary(self):
        domain = {'track_id': []}
        if self.gender == 'm':
            doamin = {'track_id': ['is_open', '=', False]}
            self.salary = 1000
            return {}
        elif self.gender == 'f':
            self.salary = 500
            return {
                'warning': {
                    'title': "Change Salary",
                    'message': 'change salary if change geneder',
                },
                'domain': domain
            }


class ItiCourseGrade(models.Model):
    _name = 'iti.course.line'
    student_id = fields.Many2one('iti.student')
    course_id = fields.Many2one('iti.course')
    grade = fields.Selection([('e', 'Excelent'),
                              ('vg', 'VeryGood'),
                              ('g', 'Good'),
                              ('p', 'Passing')])
