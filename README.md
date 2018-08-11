# attach

You can install this Python package using `pip install attach`.


## How does this work?

Here is an example session:

    >>> from attach import Namespace, attach
    >>>
    >>> foo = Namespace()
    >>> with attach(foo):
    ...    bar = 'bar'
    ...    baz = 'baz'
    ...
    >>>
    >>> bar
    Traceback (most recent call last):
        ...
    NameError: name 'bar' is not defined

Notice that since we defined `bar` inside the `attach(foo)` context, `bar` does not exist as a global.
 Instead, it's value is saved to the namespace `foo`:

    >>> foo.bar
    'bar'

We can reattach the namespace later:

    >>> with attach(foo):
    ...     print(bar)
    ...
    bar

## What’s the point?

The module is especially useful inside Jupyter notebooks. Quite often,
 we have constructions like this:
 
    X = np.array([1, 2, 3])
    def increment(X):
        return X + 1
 
In other words, we have globals and function parameters or local variables by the same name.
 However, this can lead to unintended references in the case of a typo,
 or difficulty keeping everything modular.
 
By keeping variables out of globals and inside namespaces, you can force functions to only
 use the variables that have been explicitly passed in, thereby preventing many tricky bugs!


## Isn’t hacking globals evil?

Yes, for good reason, but this is not meant to be used in code files or in production, bur rather in exploratory Jupyter notebooks.


## What’s this `Namespace` class?

You can pass any dictionary-like object into `attach()`; it does not have an instance
 of the `Namespace` class defined in this package.
 
The `Namespace` class just has a few niceties, like a nice string representation, and
 allowing you to attributes both as `foo.bar` and `foo['bar']`.


## Stuff you should know

- By default, variables beginning with an underscore are not saved to the namespace; they are lost.
   To change this behaviour, set `skip_underscored=False` in `attach()`.

- `attach()` only concerns itself with globals. If you call it inside a function,
    beware unexpected behaviour.

## To Do

- Add a `read_only` paramater to `attach()`, which enables using namespaces in a
   nested way when neeed.
- Check if being called inside a function, and error out unless `read_only=True`
   since we can’t modify function locals, only globals.
- Move tests into their own file.
