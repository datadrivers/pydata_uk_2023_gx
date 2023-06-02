# Mastering Great Expectations

PyData London, June 2023

## Initialize the configuration for local file data context

After installing GX, 

```bash
great_expectations init
```

and 

```bash
great_expectations datasource new 
```

will guide you through the setup.  
  
Note:  
* Give the source the name *source_local*
* [The CLI will dissapear in the future.](https://greatexpectations.io/blog/a-fond-farewell-to-the-cli). The context and the sources should then be created even more conveniently via Pure Python.

