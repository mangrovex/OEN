from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


def _search_age(operator, value):
    if operator not in ('ilike', '=', '>=', '>', '<', '<='):
        raise UserError(_('Invalid operator: %s' % (operator,)))

    current_date = date.today()
    last_birthday = current_date + relativedelta(years=value * -1)
    first_birthday = current_date + relativedelta(
        years=(value + 1) * -1,
        days=1,
    )
    last_possible_birthday = fields.Datetime.to_string(last_birthday)
    first_possible_birthday = fields.Datetime.to_string(first_birthday)

    if operator == '=' or operator == 'ilike':
        return ['&', ('birthdate_date', '>=', first_possible_birthday),
                ('birthdate_date', '<=', last_possible_birthday)]
    elif operator == '>=':
        return [('birthdate_date', '<=', last_possible_birthday)]
    elif operator == '>':
        return [('birthdate_date', '<', first_possible_birthday)]
    elif operator == '<=':
        return [('birthdate_date', '>=', first_possible_birthday)]
    elif operator == '<':
        return [('birthdate_date', '>', last_possible_birthday)]


class ResPartner(models.Model):
    """Partner with birth date in date format."""
    _inherit = "res.partner"

    birthdate_date = fields.Date("Birthdate")
    age = fields.Char(string="Age", readonly=True, compute="_compute_age")
    age_years = fields.Integer(
        string="Age (years old)",
        compute='_compute_age',
        search='_search_age',
    )
    place_of_birth = fields.Char(
        'Place of Birth',
        tracking=True
    )
    country_of_birth = fields.Many2one(
        'res.country',
        string="Country of Birth",
        tracking=True
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
    # CONADIS
    physical_exoneration = fields.Selection(
        [
            ('lactation', 'Lactancia'),
            ('discapacity', 'Discapacidad'),
        ],
        string=u"Exoneración Física"
    )
    conadis = fields.Char(
        string="CONADIS"
    )
    conadis_percent = fields.Percent(
        string="Porcentaje"
    )
    observation_physical = fields.Text(
        string=u'Observación'
    )
    is_deceased = fields.Boolean(
        compute='_compute_is_deceased',
    )
    date_death = fields.Datetime(
        string='Deceased Date',
    )

    @api.depends("birthdate_date")
    def _compute_age(self):
        self.compute_age_years()

    def compute_age_years(self):
        now = datetime.now()
        for record in self:
            if record.birthdate_date:
                birthdate_date = fields.Datetime.from_string(
                    record.birthdate_date,
                )
                if record.is_deceased:
                    date_death = fields.Datetime.from_string(record.date_death)
                    delta = relativedelta(date_death, birthdate_date)
                    is_deceased = _(' (deceased)')
                else:
                    delta = relativedelta(now, birthdate_date)
                    is_deceased = ''
                years_months_days = '%d%s %d%s %d%s%s' % (
                    delta.years, _('y'), delta.months, _('m'),
                    delta.days, _('d'), is_deceased
                )
                years = delta.years
            else:
                years_months_days = _('No DoB')
                years = False
            record.age = years_months_days
            if years:
                record.age_years = years

    @api.constrains('birthdate_date')
    def _check_birthdate_date(self):
        """ It will not allow birthday in the future. """
        now = datetime.now()
        for record in self:
            if not record.birthdate_date:
                continue
            birthday = fields.Datetime.from_string(record.birthdate_date)
            if birthday > now:
                raise ValidationError(_(
                    'Partners cannot be born in the future.',
                ))

    def _compute_is_deceased(self):
        for record in self:
            record.is_deceased = bool(record.date_death)

    @api.onchange('birthdate_date')
    def _onchange_birthdate_date(self):
        self.compute_age_years()
