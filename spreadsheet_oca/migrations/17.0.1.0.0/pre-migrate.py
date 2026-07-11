# Clean-room rewrite: dropped the openupgradelib (AGPL) dependency.
# 17.0 renamed spreadsheet.spreadsheet.data -> spreadsheet_binary_data (a Binary attachment field).
# openupgrade.rename_fields did: rename the ir_model_fields row, the physical column if stored, and
# the attachment rows (res_field). Reproduce that with plain cursor SQL so no third-party lib is used.


def migrate(cr, version):
    cr.execute(
        "UPDATE ir_model_fields SET name = 'spreadsheet_binary_data' "
        "WHERE model = 'spreadsheet.spreadsheet' AND name = 'data'"
    )
    # attachment-backed Binary: the value lives in ir_attachment.res_field, not a column
    cr.execute(
        "UPDATE ir_attachment SET res_field = 'spreadsheet_binary_data' "
        "WHERE res_model = 'spreadsheet.spreadsheet' AND res_field = 'data'"
    )
    # if a physical column exists (non-attachment storage), rename it too
    cr.execute(
        "SELECT 1 FROM information_schema.columns "
        "WHERE table_name = 'spreadsheet_spreadsheet' AND column_name = 'data'"
    )
    if cr.fetchone():
        cr.execute(
            'ALTER TABLE spreadsheet_spreadsheet RENAME COLUMN data TO spreadsheet_binary_data'
        )
