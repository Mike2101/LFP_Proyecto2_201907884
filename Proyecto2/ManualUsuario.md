Miguel Angel Estrada Cifuentes.<br>
Lab Lenguajes Formales y de Programación Seccion B+. <br>
Carnet: 201907884.

---------------------------------------------------------------------------------
<center>

# Manual De Usuario
</center>

## Introduccion:

 El propósito del siguiente manual es que el usuario puede usar e interactuar con la aplicacion de la mejor manera posible, para que pueda realizar las operaciones que se le solicitan.

## Ventana Inicial:
Al arrancar la aplicacion se mostrara la siguiente ventana:
![Ventana Inicial](manualUsuario/Vinicial.png)

En esta ventana se puede observar que se tiene un menu en la parte superior, el cual contiene las siguientes opciones:
* Abrir Archivo
* Guardar Archivo
* Limpiar
* Analizar
* Errores
* Tokens
* Salir

Tambien se pueden observar dos cajas de texto, la derecha mostrara la entrada, la izquierda mostrara la salida del proceso de analisis.

## Abrir Archivo:
Al seleccionar esta opcion se abrira una ventana para seleccionar el archivo que se desea abrir, el archivo puede tener la extension .txt o .lfp, si el archivo no existe se mostrara un mensaje de error

<center>

![Abrir Archivo](manualUsuario/abrir.png)
</center>

Luego se mostrara el contenido del archivo en la caja de texto de entrada, la caja de texto de salida permanece vacia hasta que se realice un analisis.
<br>
<br>
<center>

![Limpiar](manualUsuario/despuesdeabrir.png)
</center>

## Guardar Archivo:
Al seleccionar esta opcion se abrira una ventana para seleccionar el archivo donde se desea guardar el archivo, el archivo puede tener la extension .txt o .lfp, si el archivo no existe se creara uno nuevo, si el archivo ya existe se sobreescribira.


## Limpiar:
Al seleccionar esta opcion se limpiaran las cajas de texto de entrada, salida solo se actualiza despues de realizar un analisis.

si no hay contenido en la caja de texto de entrada se mostrara un mensaje de error.
<Center>

![Limpiar](manualUsuario/limpiar.png)
</Center>

## Analizar:
Al seleccionar esta opcion se analizara el contenido de la caja de texto de entrada, si no hay contenido en la caja de texto de entrada se mostrara un mensaje de error.

despues del analisis se mostrara el contenido de la caja de texto de salida.

<center>

![Analizar](manualUsuario/salida.png)
</center>

## Errores:

Al seleccionar esta opcion se mostrara una tabla dentro de una ventana con los errores que se encontraron en el analisis, si no hay errores no se mostrara nada en la tabla.

<center>

![Errores](manualUsuario/errores.png)
</center>

## Tokens:

Al seleccionar esta opcion se mostrara una tabla dentro de una ventana con los tokens que se encontraron en el analisis, si no hay tokens no se mostrara nada en la tabla.

<center>

![Tokens](manualUsuario/tkns.png)
</center>