# 🎰 SPOTGAMING  
### Sistema de Gestión y Control para Máquinas de Casino  
Desarrollado por **G-DevSolutions**

---

## 📌 Descripción General

**SPOTGAMING** es un sistema integral creado para la administración, control y seguimiento operativo de máquinas de casino, clientes, salas, instalaciones, fallas, auditorías y movimientos.  
Este proyecto representa uno de los casos de éxito iniciales de **G-DevSolutions**, enfocado en brindar soluciones tecnológicas eficientes para el sector del entretenimiento y la operación de máquinas electrónicas.

El sistema está construido con el framework **Django**, manteniendo un enfoque modular, escalable y seguro.

---

## 🚀 Características Principales

### 🎫 Gestión de Clientes
- Registro, edición y seguimiento de clientes.
- Resumen completo de datos y operaciones asociadas.

### 🏢 Administración de Salas
- Creación y configuración de salas.
- Asignación de máquinas y monitoreo operativo.

### 🎰 Control de Máquinas
- Registro de instalaciones.
- Gestión y visualización de fallas reportadas.
- Historial de mantenimientos, reparaciones y movimientos.

### 🧾 Procesos y Auditoría
- Formatos de revisión y auditoría.
- Anexos y documentos asociados.
- Registros automáticos para control interno.

### 🗄️ Almacén y Repuestos
- Inventario de repuestos y consumibles.
- Control de entradas, salidas y existencias.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+**
- **Django Framework**
- **HTML5, CSS3**
- **Bootstrap**
- **JavaScript**
- **SQLite / PostgreSQL**
- **Git / GitHub**

---

## 📂 Estructura del Proyecto (Resumen)

SPOTGAMING/
│── SPOTGAMING/ # Configuración general del proyecto Django
│── Myapp/ # Lógica de negocio principal
│ ├── templates/ # Interfaces HTML del sistema
│ ├── views.py # Vistas y controladores
│ ├── urls.py # Rutas internas
│── media/ # Archivos y documentos cargados por el sistema
│── admin-interface/ # Personalización del panel de administración
│── .gitignore # Exclusión de archivos temporales (.pyc, caches)
│── app.yaml # Configuración adicional / despliegue
│── manage.py # Ejecutor del proyecto

Clonar el repositorio
```bash
git clone https://github.com/GiovannyGarzon/spotgaming.git
cd spotgaming

Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

Instalar dependencias

pip install -r requirements.txt

Realizar migraciones

python manage.py makemigrations
python manage.py migrate

Ejecutar el servidor

python manage.py runserver

El sistema estará disponible en:
👉 http://127.0.0.1:8000/
