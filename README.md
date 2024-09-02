![Applifi](banner.webp)

<div align="center">
    <h1>Applifli</h1>
</div>

> Applifi es una app para Windows que permite a los usuarios de Windows poder descargar de la AppStore apps de Apple, en este caso se usa la herramienta creada en el lenguaje Go llamada ipatools para descargar las app.

<div align="center">
    <img src="icon_windows.ico" alt="Applifi" height="100">
</div>

<p align="center">
  <a href="https://github.com/KeimaSenpai/Applifi/releases">
    <img src="btn.webp" alt="Download" height="20">
  </a>
</p>

## 🔩Para compilar la app

- Primero debes de clonar el repo
```console
git clone https://github.com/KeimaSenpai/Script-launcher-Minecraft.git
```

- Crear entorno de desarrollo

```console
pip install virtualenv
virtualenv env
```

- Instalar dependencias

```console
pip install -r requirements.txt
```

### 🔩Instalación para los usuarios de Cuba

> Para que no gasten megas en la instalacion del paquete pueden usar este comando
> Solo funciona para CUBA este comando

```console
python -m pip install -r requirements.txt --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ --trusted-host nexus.prod.uci.cu
```

### 📦Para empaquetar

```console
flet pack  main.py --name Applifi --onedir --icon icon_windows.ico --product-name Applifi --add-data "assets;assets" --product-version "1.0.0" --copyright "Copyright (c) 2024 KeimaSenpai"
```

### 💼Personas que trabajaron
[![Contributors](https://contrib.rocks/image?repo=KeimaSenpai/Applifi)](https://github.com/KeimaSenpai/Applifi/graphs/contributors)




