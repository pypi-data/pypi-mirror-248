# About Myrrh Pyro5 Provider

This is a myrrh provider designed to test the Myrrh framework, especially in a cross-environment. This provider is divided into 2 parts: an agent (the server) to be deployed on the managed entity and a client installed on the Myrrh host.

This provider uses pyro5 for the client-server implementation and exports the API of the Myrrh local provider. (for more information: `https://github.com/irmen/Pyro5`)

/!\ This provider is intended for test purposes only and should not be deployed in an unsafe environment.

# Requirements

* Python: 3.11
* Myrrh: 0.1.0
* OS: Nt or POSIX

# Installation

## On the Myrrh controller (windows or posix):

To install the plugin, simply run:

```shell
$ pip install mplugin_provider_pyro5
```

You can create a standalone server executable using pyinstaller

```shell
$ pip install pyinstaller
$ pip install mplugin_provider_pyro5
$ myrrhc provider pyro5 pyinstaller
```

## On the target (windows or posix):
Install Python and install the mplugin_provider_pyro5 as above

Or 

Upload the pyro5s server created with pyinstaller 'dist/myrrh_pyro5s'


# Getting Started


## To launch the server on the target


```shell
$ myrrh_pyro5s --hostname 10.10.10.10 --port 9999
Server started, uri: PYRO:provider@10.10.10.10:9999
```

## Use the Myrrh framework to communicate with the server

Using python:

```python
import bmy

bmy.new(path='**/pyro5', uri='PYRO:provider@10.10.10.10:9999', eid='pyro5')  # defines an entity named "pyro5"
bmy.build(eid='pyro5')  # starts using it

# code sample
bmy.lsdir(eid='pyro5')

with bmy.select(eid='pyro5'):
    from mlib.py import os  # uses python's os module on the "pyro5" entity

os.getcwd()
```

# Using myrrh console:

```shell
$ myrrhc
 Welcome to Myrrhc Console (for test purpose only)
  - Use it with fairplay -
Type help, copyright, credits, license for more information

ctrl-D to exit console


(myrrhc)provider new pyro5 --uri PYRO:provider@127.0.0.1:9999 pyro5 && build
pyro5
entity built
 
[pyro5]
```
