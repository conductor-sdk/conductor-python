# Using Conductor in your Application
Conductor SDKs are very lightweight and can easily be added to your existing or a new python app.
In this section, we will dive deeper into integrating Conductor in your application.


## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install SDK](#install-sdk)
  - [Setup SDK](#setup-sdk)
- [Start Conductor Server](#start-conductor-server)
- [Build a conductor workflow based application](#build-a-conductor-workflow-based-application)
  - [Step 1: Create a Workflow](#step-1-create-a-workflow)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _your_ application](#step-3-write-_your_-application)
- [Implementing Workers](#implementing-workers)
  - [Design Principles for Workers](#design-principles-for-workers)
- [System Tasks](#system-tasks)
  - [Wait Task](#wait-task)
  - [HTTP Task](#http-task)
  - [Javascript Executor Task](#javascript-executor-task)
  - [Json Processing using JQ](#json-processing-using-jq)
- [Executing Workflows](#executing-workflows)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute dynamic workflows using Code](#execute-dynamic-workflows-using-code)
- [Managing Workflow Executions](#managing-workflow-executions)
  - [Get the execution status](#get-the-execution-status)
  - [Update workflow state variables](#update-workflow-state-variables)
  - [Terminate running workflows](#terminate-running-workflows)
  - [Retry failed workflows](#retry-failed-workflows)
  - [Restart workflows](#restart-workflows)
  - [Rerun a workflow from a specific task](#rerun-a-workflow-from-a-specific-task)
  - [Pause a running workflow](#pause-a-running-workflow)
  - [Resume paused workflow](#resume-paused-workflow)
- [Searching for workflows](#searching-for-workflows)
- [Handling Failures, Retries and Rate Limits](#handling-failures-retries-and-rate-limits)
  - [Retries](#retries)
  - [Rate Limits](#rate-limits)
- [Testing your workflows](#testing-your-workflows)
  - [Example Unit Testing application](#example-unit-testing-application)
- [Working with Tasks using APIs](#working-with-tasks-using-apis)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->






