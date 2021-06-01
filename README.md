Install something from another git repository.

## Quickstart:

```
python -c "$(curl -sL https://raw.githubusercontent.com/tignis/install/main/install.py)" https://.../repo.git
```

## Optional arguments:

* `--directory D` - clone to this directory instead of default (`~/workspace/org/repo/`)
* `--ref R` - checkout named git ref instead of prompting
* `--script S` - execute script from repo instead of default (`install.py`)
* `extras` - pass any remaining arguments to executed script
