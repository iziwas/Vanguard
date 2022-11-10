from odoo import models, fields


class State(models.Model):
    _name = 'vanguard.state'
    _description = 'Class to manage State response with requests'

    name = fields.Char(string="Name", required=True)
    code_response_start = fields.Integer(string="Code response start", required=True)
    code_response_end = fields.Integer(string="Code response end", required=True)
    type = fields.Selection([
        ('ok', 'OK'),
        ('error', "Error")
    ])
