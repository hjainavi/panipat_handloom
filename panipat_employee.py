from openerp.osv import fields, osv
from datetime import datetime

class panipat_employee(osv.osv):
    _name = "panipat.employee"
    
    _columns = {
                'employee_id': fields.many2one('hr.employee',string="Employee Name"),
                'scheduled_time': fields.datetime(string='Scheduled Time'),
                'scheduled_hours': fields.float(string='Scheduled Hours'),
                'crm_lead_allocated_id': fields.many2one('crm.lead.allocated'),
                }