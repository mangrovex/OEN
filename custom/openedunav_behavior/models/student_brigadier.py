from odoo import models, fields, api
from decimal import *
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class SieStudetnBehavior(models.Model):
    _name = 'sie.student.brigadier'
    _description = 'Student\'s Behavior'

    student_id = fields.Many2one('sie.student', string='Estudiante', required=True,
                                 domain="[('current_course','=',course_id)]", ondelete='restrict')
    behavior_id = fields.Many2one('sie.brigadier_note', string='ID Comportamiento',
                                  ondelete='cascade')
    note_brigadier = fields.Float(string="Nota", digits=dp.get_precision('Score'))
    _order = 'student_id'

    @api.multi
    @api.constrains('note_brigadier')
    def validate_note_brigadier(self):
        for record in self:
            if record.note_brigadier < 0.0 or record.note_brigadier > 20:
                raise ValidationError(record.student_id.name + ' revisar Nota ' + str(record.note_brigadier))

