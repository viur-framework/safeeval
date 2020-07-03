# safeeval

Safely evaluate an expression from an untrusted party

## Getting Started

Simply install via pip:
    
    pip install safeeval

### Prerequisites

No dependencies are required.

## Example

Simple Comparision:

    import safeeval
    ast = safeeval.SafeEval.parse("x == y")
    res = safeeval.SafeEval.evalAst(ast, {"x": 4, "y": 3)
    print("res", res)
    
    
More examples can be found in tests directory.

## Contributing

Write issues and provide patches via PRs on github.

## Authors

* **Tobias Steinrücken** - *Initial work* - [Mausbrand Informationsysteme GmbH](https://github.com/viur-framework/safeeval)

See also the list of [contributors](https://github.com/viur-framework/safeeval/blob/master/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
