# Cripto-1Q2023 Grupo 9
### MakeFile
Descarga las dependencias necesarias usando `./build.sh`
### Ejecucion
`py ./main.py {r|d} imagenSecreta k directorio`

Donde:
- {d|r}: Operacion a realizar. d para distribuir, r para recuperar
- imagenSecreta: Nombre de el archivo de la imagen secreta
- k: minimo de sombras para recuperar el secreto en un esquema (k, n)
- directorio: Directorio que contiene las carriers

### Ejemplo
```py -m .\src\main.py r yoda.bmp 6 ./images```

```py -m .\src\main.py d yoda.bmp 6 ./images```
