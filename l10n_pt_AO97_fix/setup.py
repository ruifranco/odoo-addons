# -*- coding: utf-8 -*-
from openerp import models, api

class Setup(models.Model):
	_name = "l10n_pt_ao97_fix.setup"

	@api.model
	def fix_translation(self):
		txtSQL = "	UPDATE	ir_translation \
					SET	value = REPLACE(value, 'ontat','ontact') \
					WHERE	lang LIKE 'pt_PT' \
					AND	( \
						src LIKE '%contact%' \
						OR src LIKE '%Contact%' \
						);"
		self._cr.execute(txtSQL)
		return True
