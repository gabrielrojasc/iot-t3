# Tarea 3 IoT

Integrantes:

- Alfredo Escobar
- Gabriel Rojas
- Nicolas Santibañez

## Como correr el programa

### ESP

Para correr el codigo de la esp, se debe ir a la carpeta esp32 y correr:

```bash
cd esp32 && idf.py build flash monitor
```

### Raspberry

Paquetes necesarios (pip):

- [bleak](https://bleak.readthedocs.io/en/latest)
- [Requerimientos de base de interfaz](./raspberry/interface/requirements.txt)

Para correr el codigo de la raspberry, se debe correr lo siguiente:

```bash
python3 rasberry/main.py
```
