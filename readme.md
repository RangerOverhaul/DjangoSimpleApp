# README
## Prueba Tecnica 
Github [Respo](https://djecrety.ir/)
### Requirements
|     Platform      |        Language         |
|:-----------------:|:-----------------------:|
| [Docker][V26.1.0] | [language][python_3.11] |


### Preparacion
En el archivo /PT/.env debe usar una secrect key para poder ejecutar correctamente la api.
Puedes generarla [aqui](https://github.com/RangerOverhaul/DjangoSimpleApp)
### Installation
#### Dcoker
Si tiene instalado docker en su sistema solo debe ejecutar:
~~~ bash
docker compose up --build -d
~~~
- Nota: Para poder ingresar al administrador de Django debe crear su propio usuario, para esto ejecute el comando:
    ~~~ bash
        docker exec -it pt-web-1 bash
        python manage.py createsuperuser
    ~~~  
#### Local
Si desea la instalacion en local debe de hacer los siguientes pasos:
~~~ bash
python -m venv myenv
source myenv/bin/activate
pip install requirements.txt
python manage.py createsuperuser

sudo chmod 777 entrypoint.sh
./entrypoint.sh o sh entrypoint.sh
~~~

La api estara activa en http://127.0.0.1:8000

### urls
- /admin/
- /v1/api/register/ (Crear nuevo usuario)
- /v1/api/login/ (Loguearse)
- /v1/api/logout/ (Desloguearse)
- /v1/api/product/create/ (Crear nuevo producto)
- /v1/api/product/update/ (Actualizar producto)
- /v1/api/product/delete/<int:pk>/ (Eliminar producto)
- /v1/api/product/get/<int:pk>/ (Detalles del producto)
- /v1/api/product/getimg/<int:pk>/ (Obtener imagen de un producto)

### Unit Testing
Para ejecutar las pruebas unitarias se debe tener la aplicacion configurada en [local](#Local), y ejecutar el siguiente comando:
~~~ bash
python manage.py test api
~~~  

## Author
Danilo Herazo.
