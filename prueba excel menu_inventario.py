from openpyxl import Workbook

def crear_excel(inventario):
    wb = Workbook()
    hoja = wb.active
    hoja.title = "Inventario de Hilos"

    # Encabezados de las columnas
    encabezados = ["Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"]
    hoja.append(encabezados)

    for hilo in inventario:
        hoja.append([
            hilo["marca"],
            hilo["codigo_color"],
            hilo["descripcion"],
            hilo["cantidad"],
            hilo["precio_unitario"],
            hilo["proveedor"]
        ])

    wb.save("inventario_hilos.xlsx")
    print("Archivo 'inventario_hilos.xlsx' creado con éxito.")