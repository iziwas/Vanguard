from odoo import models, fields


class State(models.Model):
    _name = 'vanguard.state'
    _description = 'Class to manage State response with requests'

    name = fields.Char(string="Name", required=True)
    code_response = fields.Integer(string="Code", required=True)
    type = fields.Selection([
        ('ok', 'OK'),
        ('error', "Error")
    ])
