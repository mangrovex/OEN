# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


class SieCreateStudent(models.TransientModel):
    _name = 'sie.create.student'
    _description = "Create student"

    cedula = fields.Char(
        "Cedula",
        required=True
    )

    def create_student(self):
        for record in self:
            student = self.env['sie.student'].search([('ced_ruc', '=', record.cedula)])
            db_model = self.env['base.external.dbsource'].search([('name', '=', 'Personal')])
            query = "select * from consultadigedo.v_personal_mil_dir where cedula = '" + record.cedula + "' "
            res = db_model.execute(query)
        if student:
            raise Warning("El estudiante ya existe")
        action = self.env.ref('openedunav_core.act_open_sie_student_view').read()[0]
        action['view_mode'] = 'form'
        action['views'] = [(self.env.ref('openedunav_core.sie_student_view_form').id, 'form')]
        action['res_id'] = 18
        return action
