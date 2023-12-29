# Ender's Utils
## How to use:
### `from endersutils import endersutils`
Would recommend using `as` to make it easier
### `from endersutils import endersutils as eu`
It will be shown as `eu` throughout the docs so that is all the explanation you're getting

## `eu.fixedrange`:
### Returns a range with a bias of one (I.E. `range(3)` returns `(0, 1, 2)` whereas `fixedrange(3)` returns `(1, 2, 3)`)

## `eu.fixedindex`:
### Its like one of those python tutorials where it just adds 1 to a number but I did it for some reason. No docs, just timewasting

## `eu.version`:
### Returns the version in [Semantic Versioning](https://en.wikipedia.org/wiki/Software_versioning#Semantic_versioning)

## `eu.intversion`:
### Returns the main integer version, used so I can exclude main versions but small bug-fixes will stay the same and I don't have to specify 1000 version rules

## `eu.pair()`:
### Returns a name-value pair at `obj[0]` for name and `obj[1]` for the value(assuming obj is equal to `eu.pair()`)

## `eu.components()`:
### Returns a manager class for components
Methods:
    - `add_component(func, params)`: Adds a function component and passes in `params`. Stores at the next available index starting at 0 of the `eu.components` class
    - `run_component(idx)`: Runs the command stored at `idx`
    - `del_component(idx)`: Deletes the command at the specified index and pushes the ones behind it down
    - `list_components()`: Prints a neatly formatted version of all the components in a class. (Doesn't return the list, do `eu.components.component`)