# Using Conductor in your Application
Conductor SDKs are very lightweight and can easily be added to your existing or a new python app.
In this section, we will dive deeper into integrating Conductor in your application.


## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Adding Conductor SDK to your application](#adding-conductor-sdk-to-your-application)
- [Managing Workflow & Task definitions](#managing-workflow--task-definitions)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Adding Conductor SDK to your application
Conductor Python SDKs are published on PyPi @ https://pypi.org/project/conductor-python/

```shell
pip3 install conductor-python
```

## Managing Workflow & Task definitions

> [!tip]
> Treat your workflow definitions just like your code.
> If you are defining the workflows using UI, we recommend checking in the JSON configuration into the version control
> and using your development workflow for CI/CD to promote the workflow definitions across various environments such as Dev, Test and Prod.






