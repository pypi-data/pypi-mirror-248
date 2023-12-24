from django.db.models import Q

def execute_database_query(
    model,
    filter_kwargs,
    excluded_q,
    columns,
    search_item=None,
    column_mapping=None,
    table_filters=None,
    table_sort=None,
):
    """
    Execute a database query based on the provided parameters.

    Args:
        model (django.db.models.Model):
            The model class representing the database table.
        filter_kwargs (dict):
            The filter arguments for the database query.
        excluded_q (django.db.models.Q):
            The exclusion query for filtering out specific records.
        columns (list):
            The columns to select from the database table.
        search_item (str, optional):
            The search term to filter the data. Defaults to None.
        column_mapping (dict, optional):
            The mapping of column names between the model and the exported file.
            Defaults to None.
        table_filters (str, optional):
            Additional table filters to apply to the data.
            Multiple filters can be separated by ":::".
            Each filter should follow the format "column_name___filter_type___filter_value".
            Defaults to None.
        table_sort (str, optional):
            The column name to sort the data by, with an optional leading hyphen (-)
            for descending order. Defaults to None.

    Returns:
        QuerySet:
            The query result representing the filtered and sorted data.
    """

    # COLUMN MAPPING
    if column_mapping:
        # Change columns to the value from column_mapping if it matches a key
        columns = [column_mapping.get(col, col) for col in columns]

    # query result
    rows = model.objects.filter(Q(**filter_kwargs) & ~excluded_q)

    # SEARCH
    if search_item:
        search_item = search_item.strip()
        search_conditions = Q()
        for column in columns:
            search_conditions |= Q(**{f"{column}__icontains": search_item})
        rows = rows.filter(search_conditions)
    # FILTER
    if table_filters:
        condition_mapping = {
            "iexact": ("iexact", "{}"),
            "isnot_iexact": ("iexact", "{}"),
            "gt": ("gt", "{}"),
            "gte": ("gte", "{}"),
            "lt": ("lt", "{}"),
            "lte": ("lte", "{}"),
            "icontains": ("icontains", "{}"),
            "noticontains": ("icontains", "{}"),
            "istartswith": ("istartswith", "{}"),
            "iendswith": ("iendswith", "{}")
        }
        filter_conditions = Q()
        filter_items = table_filters.split(":::")
        for filter_item in filter_items:
            selected_column, selected_condition, value = filter_item.split("___")
            selected_column = column_mapping.get(selected_column, selected_column)
            lookup, format_string = condition_mapping.get(selected_condition, (None, None))
            if selected_column and lookup and value:
                field_lookup = f"{selected_column}__{lookup}"
                condition = Q(**{field_lookup: format_string.format(value)})
                # Handle "isnot_iexact" and "noticontains" conditions
                if selected_condition in ["isnot_iexact", "noticontains"]:
                    condition = ~condition
                filter_conditions &= condition
        rows = rows.filter(filter_conditions)
    # SORT
    if table_sort:
        sort_fields = table_sort.split(",")
        for sort_field in sort_fields:
            column_name = sort_field.lstrip('-')
            if column_name in column_mapping:
                column_name = column_mapping[column_name]
            if sort_field.startswith("-"):
                rows = rows.order_by('-' + column_name)
            else:
                rows = rows.order_by(column_name)
    # return result query
    return rows
