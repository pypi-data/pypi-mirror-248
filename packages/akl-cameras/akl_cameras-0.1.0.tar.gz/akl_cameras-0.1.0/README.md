# AKL Cameras

Tool that allow to operate cameras owned by AKL.

## Instalation

### Install required package

*Manjaro:*

```bash
$ sudo pamac install gphoto2
```

*Fedora:*

```bash
$ sudo dnf install gphoto2
```

*RaspberyPi:*

```bash
$ sudo apt install gphoto2
```

### Setup repository

```bash
$ git clone git@gitlab.com:academic-aviation-club/droniada-2024/akl-cameras.git
$ cd akl-cameras
$ poetry install --no-root
$ poetry shell
```

### Setup repository on RaspberyPi:

```bash
$ git clone git@gitlab.com:academic-aviation-club/droniada-2024/akl-cameras.git
$ cd akl-cameras
```

### Hardware preparation

1. Connect camera to the on-board computer,