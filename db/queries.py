from db.db_connection import connect_db

def get_materials(filters):
    connection = connect_db()
    cursor = connection.cursor()

    query = """
        SELECT 
            m.titel_material AS title, 
            m.price, 
            m.storage_quantity AS stock_quantity, 
            m.min_quantity, 
            t.title_mtype AS type, 
            s.title_supplier AS supplier, 
            m.picture
        FROM materials m
        LEFT JOIN mtype t ON m.mtype_id = t.id_mtype
        LEFT JOIN materials_suppliers ms ON m.id_material = ms.material_id
        LEFT JOIN suppliers s ON ms.supplier_id = s.id_supplier
    """
    conditions = []

    # поисковой фильтр
    if filters.get("search"):
        conditions.append(f"(m.titel_material ILIKE '%{filters['search']}%' OR s.title_supplier ILIKE '%{filters['search']}%')")

    # сток фильтр
    if filters.get("stock") == 1:
        conditions.append("m.storage_quantity > 0")
    elif filters.get("stock") == 2:
        conditions.append("m.storage_quantity = 0")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # сортировка
    sort_options = [None, "m.titel_material", "t.title_mtype", "m.price", "s.title_supplier"]
    sort_by = sort_options[filters.get("sort_by")]
    if sort_by:
        query += f" ORDER BY {sort_by}"

    # пагинация
    offset = (filters["page"] - 1) * filters["items_per_page"]
    query += f" LIMIT {filters['items_per_page']} OFFSET {offset}"

    cursor.execute(query)
    rows = cursor.fetchall()

    materials = [
        {
            "title": row[0],
            "price": row[1],
            "stock_quantity": row[2],
            "min_quantity": row[3],
            "type": row[4],
            "supplier": row[5],
            "picture": row[6],
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return materials
