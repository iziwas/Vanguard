from odoo import models, fields, api


class Time(models.Model):
    _name = 'vanguard.time'
    _description = "Class to manage time between 2 tests for a client"

    minutes = fields.Integer(string="Time between two tests (in minutes)")
    name = fields.Char(string="Name", compute="_compute_name", store=True)

    @api.depends('minutes')
    def _compute_name(self):
        for rec in self:
            rec.name = str(rec.minutes)
