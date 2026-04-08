
import pandas as pd

# 1. Crear el conjunto de datos de ventas de coches
datos = {
    'Vendedor': ['Elena', 'Marco', 'Elena', 'Sofía', 'Marco', 'Sofía', 'Elena', 'Marco'],
    'Modelo': ['Sedán', 'SUV', 'Pickup', 'Sedán', 'Sedán', 'SUV', 'SUV', 'Pickup'],
    'Precio_Venta': [450000, 350000, 450000, 220000, 240000, 380000, 320000, 480000],
    'Comision_Pactada': [0.05, 0.04, 0.06, 0.05, 0.05, 0.04, 0.04, 0.06]
}

df_ventas = pd.DataFrame(datos)

# 2. Calcular la comisión en dinero por cada venta
df_ventas['Monto_Comision'] = df_ventas['Precio_Venta'] * df_ventas['Comision_Pactada']

# 3. Agrupar por Vendedor para obtener las estadísticas
# El método .agg() (abreviatura de aggregate)
stats_vendedores = df_ventas.groupby('Vendedor').agg(
    Coches_Vendidos=('Modelo', 'count'),
    Total_Ingresos=('Precio_Venta', 'sum'),
    Promedio_Venta=('Precio_Venta', 'mean'),
    Total_Comisiones=('Monto_Comision', 'sum')
).reset_index()

# 4. Añadir una métrica de "Ticket Promedio" formateada
stats_vendedores['Ticket_Promedio'] = stats_vendedores['Total_Ingresos'] / stats_vendedores['Coches_Vendidos']

# 5. Ordenar de mayor a menor ingreso
stats_vendedores = stats_vendedores.sort_values(by='Total_Ingresos', ascending=False)

# Mostrar resultados
print("--- Listado de Ventas Individuales ---")
print(df_ventas.head())

print("\n--- Estadísticas Finales por Vendedor ---")
print(stats_vendedores)
