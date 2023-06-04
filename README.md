# Mastering Great Expectations

<img src="https://images.squarespace-cdn.com/content/v1/62ebd8e38f68d651ae7892a2/9def1f60-daba-4ff6-838f-ea9bcfc7ee6d/PyData_logo.png?format=1500w" width="30%" height="30%">

London, June 2023

## Initialize the configuration for local file data context

After setting up the virtual environment, go for

```bash
great_expectations init
```

and 

```bash
great_expectations datasource new 
```

This will guide you through the setup.  
  
Note:  
* Give the source the name *source_local*, so that it the configuration is consistent to the notebook.
* [The CLI will dissapear in the future.](https://greatexpectations.io/blog/a-fond-farewell-to-the-cli). The context and the sources should then be created even more conveniently via Pure Python.

## Q & A

A few questions from the memory log

### What are the options for handling Data Drift?

In many expectations there is the possibility to pass the parameter *mostly*. 
Deviations can thus be allowed to a certain extent. 
The so-called evaluation parameters also allow to reference a validation run with results of a previous one.
This allows a step change in metrics to be tolerated if one so chooses. 

### How does this framework reference to packages like panderas and pydantic?

These packages are for testing data structure expectations directly in the code. In my view, this is a separate use case. As we have seen in the flowchart, we want to check the data exactly at the intermediate points between the processing steps.
The whole point is not that the code breaks at runtime, but that validation is done upstream.

### For data terrabytes in size and up, query execution can get expensive. What does this mean for validation?

This is an issue regardless of the tool chosen. The tradeoff between the cost of validation and the gain from early detection of unexpected data must be evaluated individually.

