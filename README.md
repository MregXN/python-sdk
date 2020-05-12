# Dapr SDK for Python

## Structure of Python SDK

* [dapr/actor](./dapr/actor): Actor Framework
* [dapr/clients](./dapr/clients): HTTP clients for Dapr building blocks
* [dapr/serializers](./dapr/serializers): serializer/deserializer
* [dapr/conf](./dapr/conf): Configuration
* [flask_dapr](./flask_dapr): flask extension for Dapr
* [tests](./tests/): unit-tests
* [examples/demo_actor](./examples/demo_actor): demo actor example

## Status - Phase 1

* [x] Initial implementation of Actor Runtime/Manager/Proxy
* [x] Actor service invocation
* [x] RPC style actor proxy
* [x] Flask integration for Dapr Actor Service
* [x] Example for Actor service invocation
* [x] Complete tox.ini setup
* [x] Actor state management
* [x] Actor timer
* [x] Actor reminder
* [x] Enhance error handling
* [ ] Improve documents in code
* [ ] Generate documents using sphinx
* [ ] Publish dapr-python package

## Status - Phase 2

* [ ] Create convinient layer wrapping gRPC and HTTP clients for Dapr
* [ ] Flask extensions for Dapr State/Pubsub/Bindings

## Developing

### Prerequisites

* [Install Dapr standalone mode](https://github.com/dapr/cli#install-dapr-on-your-local-machine-standalone)
* [Install Python 3.8+](https://www.python.org/downloads/)

### Build and test

1. Clone python-sdk

```bash
git clone https://github.com/dapr/python-sdk.git
cd python-sdk
```

2. Install required packages

```bash
pip3 install -r dev-requirements.txt
```

3. Set PYTHONPATH environment

```bash
export PYTHONPATH=`pwd`
```

4. Run unit-test

```bash
tox -e py38
```

## Examples

* [DemoActor example](./examples/demo_actor)
* Dapr service invocation examples
  - [invoke-simple](./examples/invoke-simple)
  - [invoke-custom-data](./examples/invoke-custom-data)
* [Dapr Pubsub example](./examples/pubsub-simple)
