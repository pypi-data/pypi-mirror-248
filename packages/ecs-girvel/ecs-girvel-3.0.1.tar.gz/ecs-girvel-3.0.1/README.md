[//]: # (TODO mention minimalistic & does not presume anything, maximal compatibility)

# ECS micro-engine

Library for python containing an interpretation of ECS design pattern. 

## Features

1. Adding/removing entity's attributes causes dynamic addition/removal of the entity from the corresponding systems
2. Systems with annotation-based syntax
3. Asynchronous systems (yield skips a frame)
4. Systems accept multiple arguments, preventing global mutable state issues
5. Full compatibility with type hints

## Interpretation

1. Entity is a python object
2. Component is entity's attribute
3. System is an entity describing an interaction between cartesian product of entities
4. Metasystem is a system that launches other systems
5. MetasystemFacade encapsulates all general logic (add, remove, update)

## Installation

```bash
pip install ecs-girvel
```

## Usage

You can also see [girvel/fallen](https://github.com/girvel/fallen), ecs is written for it.

```py
from ecs import MetasystemFacade, System, Entity  # TODO NEXT fix demo
import time


# 1. You create a metasystem
ms = MetasystemFacade()

dt = 0.04

# 2. You create systems and add them to metasystem
class VerticalSpeed:
    vy: float

class GravityConstants:
    g: float

@ms.add
@System
def gravity(target: VerticalSpeed, constants: GravityConstants):
    target.vy += constants.g * dt

class Inert:
    x: float
    y: float
    vx: float
    vy: float

@ms.add
@System
def inertia(target: Inert):
    target.x += target.vx * dt
    target.y += target.vy * dt

class Displayable:
    x: float
    y: float
    name: str

@ms.add
@System
def output(target: Displayable):
    yield from range(int(1 / dt) - 1)  # skips 24 out of 25 frames
    print(f'{target.name}: {target.x:.2f}, {target.y:.2f}')


# 3. You create objects
class DynamicEntity(Entity):
    def __init__(self, **attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

ms.add(DynamicEntity(name='falling_guy1', x=0, y=0, vx=0, vy=0))
ms.add(DynamicEntity(name='falling_guy2', x=100, y=0, vx=0, vy=0))
ms.add(DynamicEntity(g=10))


# 4. Game loop
if __name__ == "__main__":
    while True:
        ms.update()
        time.sleep(dt)
```