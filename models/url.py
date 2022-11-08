import requests
import logging

from odoo import models, fields, api, Command
from datetime import timedelta


_logger = logging.getLogger("vanguard.url")


class Url(models.Model):
    _name = 'vanguard.url'
    _description = 'Model to manage URL to check'

    url_to_check = fields.Char(string="Url", required=True)
    partner_id = fields.Many2one("res.partner", string="Clients")
    time_between_test = fields.Many2one("vanguard.time", string="Time between two tests")
    minutes = fields.Integer(related="time_between_test.minutes", readonly=True)
    state_id = fields.Many2one("vanguard.state", string="State")
    state_type = fields.Selection(related="state_id.type", readonly=True)
    last_checked = fields.Datetime(string="Last checked", readonly=True)
    next_check = fields.Datetime(string="Next check", compute="_compute_next_check", store=True)
    test_ids = fields.One2many("vanguard.test", "url_id", string="Tests")
    active = fields.Boolean(string="Active", default=True)

    def name_get(self):
        return [(rec.id, "{} [{}]".format(rec.partner_id.name, rec.url_to_check or "")) for rec in self]

    @api.depends('last_checked', 'time_between_test', 'time_between_test.minutes')
    def _compute_next_check(self):
        """
        Compute to check the next time we triggered a test for this URL.
        """
        for rec in self:
            minutes_to_add = rec.minutes
            if rec.state_id.type == 'error':
                minutes_to_add = self.env.ref("vanguard.time_5").minutes

            if minutes_to_add:
                rec.next_check = (rec.last_checked or fields.Datetime.now()) + timedelta(minutes=minutes_to_add)
            else:
                rec.next_check = False

    def _cron_url_to_check(self):
        datetime_called = fields.Datetime.now()

        urls_to_check = self.env['vanguard.url'].search([
            ('next_check', '<=', datetime_called)
        ])

        if not urls_to_check:
            _logger.info("No url to check at : " + datetime_called.strftime("%d/%m/%Y, %H:%M:%S"))

        for url in urls_to_check:
            url_state = url.state_type

            try:
                r = requests.get(url.url_to_check)
                status_code = r.status_code
            except requests.HTTPError as e:
                status_code = e.response.status_code
            except requests.exceptions.SSLError:
                status_code = 495

            # Research the state object with status_code
            state = self.env['vanguard.state'].search([('code_response', '=', status_code)])
            if not state:
                state = self.env['vanguard.state'].create({
                    'name': status_code,
                    'code_response': status_code,
                    'type': 'error'
                })

            # Create Test object
            self.env['vanguard.test'].create({
                'date_check': datetime_called,
                'state_id': state.id,
                'url_id': url.id,
            })

            # Update url datas
            url.last_checked = datetime_called
            url.state_id = state.id

            _logger.info("Checked : " + url.url_to_check + " - " + str(status_code))
            if url_state == 'error' and state.type == 'error':
                _logger.info("Email sent : " + url.url_to_check)
                url.email_should_be_sent()

            if url_state == "error" and state.type == "ok":
                url.email_should_be_sent(in_error=False)

    def email_should_be_sent(self, in_error=True):
        self.ensure_one()
        partner_ids = ""

        template = self.env.ref("vanguard.vanguard_template_server_down")
        if not in_error:
            template = self.env.ref("vanguard.vanguard_template_server_up")

        for p in self.partner_id.vanguard_partner_ids:
            if partner_ids:
                partner_ids += ","
            partner_ids = str(p.id)

        template.partner_to = partner_ids
        template.send_mail(self.id, force_send=True)



