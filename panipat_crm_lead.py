from openerp.osv import fields, osv
from datetime import datetime

AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]

class panipat_crm_lead(osv.osv):
    _name = "panipat.crm.lead"
    _rec_name = 'sequence'
    
    def write(self,cr,uid,ids,vals,context=None):
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^",id,vals
        return super(panipat_crm_lead,self).write(cr,uid,ids,vals,context=None)
    
    def create(self,cr,uid,vals,context=None):
        if vals.get('sequence','/')=='/':
            print "in sequnece"
            vals['sequence']=self.pool.get('ir.sequence').get(cr,uid,'CRM.Lead.Order.No',context=None) or '/'
        print "valssssssssssssssssssssssssssssssss",vals
        return super(panipat_crm_lead,self).create(cr,uid,vals,context=None)
    
    def confirm_and_allocate(self,cr,uid,id,context=None):
        self.write(cr,uid,id,{'state':'done'},context=None)
        carry_fields = self.read(cr,uid,id,['sequence','partner_id'],context=None)
        print "carry fields.......................................",carry_fields
        crm_id = carry_fields[0].pop('id')
        vals=carry_fields[0]
        if vals.get('partner_id',False) :
            vals['partner_id'] = vals.get('partner_id')[0]
        vals['sequence'] = crm_id
        vals.update({'state':'draft'})
        print "---------------",vals
        
        allocated_id=self.pool.get('crm.lead.allocated').create(cr,uid,vals,context=None)
        print "---------------=================",allocated_id
        return {
            'name': 'CRM - Leads Allocated Form',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.lead.allocated',
            'type': 'ir.actions.act_window',
            'res_id': allocated_id,
        }
                                                  
    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            values = {
                'partner_name': partner.parent_id.name if partner.parent_id else partner.name,
                'contact_name': partner.name if partner.parent_id else False,
                'title': partner.title and partner.title.id or False,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id and partner.state_id.id or False,
                'country_id': partner.country_id and partner.country_id.id or False,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'fax': partner.fax,
                'zip': partner.zip,
            }
        return {'value': values}

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id=self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id}}
        return {}
    
    _columns = {
        'partner_name': fields.char(string="Company Name"),
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='set null', track_visibility='onchange',
            select=True, help="Linked partner (optional). Usually created when converting the lead."),
        'name': fields.char('Subject', required=True, select=1),
        'email_from': fields.char('Email', size=128, help="Email address of the contact", select=1),
        'create_date': fields.datetime('Creation Date', readonly=True),
        'description': fields.text('Notes'),
        'contact_name': fields.char('Contact Name', size=64),
        'priority': fields.selection(AVAILABLE_PRIORITIES, 'Priority', select=True),
        'user_id': fields.many2one('res.users', 'Salesperson', select=True, track_visibility='onchange'),
        'current_date': fields.datetime('Date',Readonly=True),
        'product_line': fields.one2many('panipat.crm.product','crm_lead_id',string="Products"),
        'street': fields.char('Street'),
        'street2': fields.char('Street2'),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City'),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'phone': fields.char('Phone'),
        'fax': fields.char('Fax'),
        'mobile': fields.char('Mobile'),
        'title': fields.many2one('res.partner.title', 'Title'),
        'sequence': fields.char(string="Order No."),
        'state': fields.selection(string="State",selection=[('draft','Draft'),('done','Done')]),
    }

    _defaults = {
        'create_date': fields.datetime.now,
        'sequence':'/',
        'state': 'draft',
    }