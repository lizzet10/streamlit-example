import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi

# Título de la aplicación
st.title("Prueba de conexión a MongoDB")

# Función para establecer la conexión a MongoDB
@st.experimental_singleton(suppress_st_warning=True)
def connection():
    return MongoClient("mongodb+srv://" + st.secrets["DB_USERNAME"] + ":" + st.secrets["DB_PASSWORD"] +
                       "@prediccion2024.xcpbxzg.mongodb.net/", tlsCAFile=certifi.where())

# Función para obtener los datos de la base de datos
@st.experimental_memo(ttl=60)
def get_data():
    db = connection().get_database("Prediccion")
    collection = db.get_collection("ejemplo2")
    items = collection.find()
    return list(items)
#

# Función para insertar datos en la base de datos
def insert_data(data):
    db = connection().get_database("Prediccion")
    collection = db.get_collection("ejemplo2")
    collection.insert_one(data)
    st.success("Datos agregados exitosamente a MongoDB")

# Obtener los datos de MongoDB
data = get_data()

# Convertir los datos al formato adecuado
formatted_data = []
for d in data:
    formatted_data.append({
        '_id': str(d['_id']),
        'Bebida': d.get('Bebida', ''),
        'Comida': d.get('Comida', ''),
        'Postre': d.get('Postre', ''),
        'Total': d.get('Total', '')
    })

# Crear DataFrame con los datos y especificar los tipos de datos
df = pd.DataFrame(formatted_data, dtype='object')

# Convertir cadenas vacías en NaN en la columna Total
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

# Mostrar los datos en una tabla
st.subheader("Datos desde MongoDB")
st.table(df)

# Formulario para agregar nuevos datos
st.subheader("Agregar nuevos datos")

# Recolección de información del usuario
new_data = {}
new_data['Bebida'] = st.text_input("Bebida")
new_data['Comida'] = st.text_input("Comida")
new_data['Postre'] = st.text_input("Postre")
new_data['Total'] = st.number_input("Total")

# Botón para insertar los nuevos datos
if st.button("Agregar"):
    insert_data(new_data)



dfInventory = pd.read_csv("datos/Inventory.csv")
st.dataframe(dfInventory.head())

inventoryCollection = dfInventory.to_dict()