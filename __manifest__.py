#-*- coding: utf-8 -*-

{
	"name": "Report Balance",
	"version": "1.0", 
	"depends": [
		'base','account','mrp'
	],
	'author': 'firmanrizaldiyusup@gmail.com',
	'website': 'http://www.vitraining.com',
	"summary": "vit_report_balanced",
	"description": """

vit_report_balanced

""",
	"data": [
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/report_balance.xml",
		"data/work_order.xml",
		"data/report_balance.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}