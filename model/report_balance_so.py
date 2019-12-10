#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class report_balance_so(models.Model):

    _name = "vit.report_balance_so"
    
    
    product_code = fields.Char( string="Product code", 
    related='product_id.default_code',
    )
    
    
    total_so_bln_lalu = fields.Float( string="Total so bln lalu",  help="")
    total_so_bulan_ini = fields.Float( string="Total so bulan ini",  help="")
    onhand = fields.Float( string="Onhand",  help="")
    heading = fields.Float( string="Heading",  help="")
    rolling = fields.Float( string="Rolling",  help="")
    furnace = fields.Float( string="Furnace",  help="")
    plating = fields.Float( string="Plating",  help="")
    fq = fields.Float( string="Fq",  help="")
    wip_on_hand = fields.Float( string="WIP",  help="")
    
    balance_so = fields.Float( string="Balance",  help="")


    report_id = fields.Many2one(comodel_name="vit.report_balance",  string="Report",  help="")
    product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")

    