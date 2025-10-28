#Registrar compra o reabastecimiento (entrada)
def registrar_compra():
    print("\n--- Registrar compra/reabastecimiento ---")
    codigo = input("Código de color del hilo: ")
    cantidad = int(input("Cantidad comprada: "))
    costo_unitario = float(input("Costo por unidad: "))

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            hilo["cantidad"] += cantidad
            historial_compras.append({
                "codigo_color": codigo,
                "marca": hilo["marca"],
                "descripcion": hilo["descripcion"],
                "cantidad": cantidad,
                "costo_unitario": costo_unitario,
                "total": cantidad * costo_unitario
            })
            print("Compra registrada y cantidad actualizada.")
            return
    print("Hilo no encontrado en el inventario.")

#Reportes y consultas
def reportes():
    print("\n--- Reportes y Consultas ---")
    print("1. Reporte general de inventario")
    print("2. Reporte por marca")
    print("3. Historial de ventas")
    print("4. Historial de compras")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        mostrar_inventario()
    elif opcion == "2":
        marca = input("Ingrese la marca a consultar: ").lower()
        encontrados = [h for h in inventario if marca in h["marca"].lower()]
        if encontrados:
            for h in encontrados:
                print(f"Marca: {h['marca']} | Código: {h['codigo_color']} | "
                      f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                      f"Precio: Q{h['precio_unitario']}")
        else:
            print("No se encontraron hilos con esa marca.")
    elif opcion == "3":
        print("\n--- Historial de Ventas ---")
        if not historial_ventas:
            print("No hay ventas registradas.")
        else:
            for v in historial_ventas:
                print(f"Marca: {v['marca']} | Código: {v['codigo_color']} | "
                      f"Descripción: {v['descripcion']} | Cantidad: {v['cantidad']} | "
                      f"Total: Q{v['total']:.2f}")
    elif opcion == "4":
        print("\n--- Historial de Compras ---")
        if not historial_compras:
            print("No hay compras registradas.")
        else:
            for c in historial_compras:
                print(f"Marca: {c['marca']} | Código: {c['codigo_color']} | "
                      f"Descripción: {c['descripcion']} | Cantidad: {c['cantidad']} | "
                      f"Costo unitario: Q{c['costo_unitario']:.2f} | Total: Q{c['total']:.2f}")
    else:
        print("Opción no válida.")