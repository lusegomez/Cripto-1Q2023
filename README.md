# Cripto-1Q2023 Grupo 9
### Ejecucion
Posicionarse en el directorio `src/`
Luego correr el siguiente comando (Reemplazando X por el numero k deseado):
`make run ARGS="<r/d> <image.bmp> <X> <./images/kX>"`

Donde:
- <r/d>: Operacion a realizar. d para distribuir, r para recuperar
- <image.bmp>: Nombre de el archivo de la imagen secreta
- <X>: minimo de sombras para recuperar el secreto en un esquema (k, n)
- <images/kX>: Directorio que contiene las carriers, en nuestro caso las imagenes se encuentran en `src/images/`

### Ejemplo de ejecucion:
```make run ARGS="r image.bmp 3 ./images/k3/"```
