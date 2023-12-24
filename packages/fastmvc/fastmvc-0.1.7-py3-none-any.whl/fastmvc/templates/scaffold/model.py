from fastmvc.models.database.^{platform.data_model_import}^


class ^{Obj}^(^{platform.data_model}^):
    key: str or None = None  # this field is required
    ^{model_attrs}^

    model_config = {
        'table_name': "^{proj}^_^{obj}^"
    }
