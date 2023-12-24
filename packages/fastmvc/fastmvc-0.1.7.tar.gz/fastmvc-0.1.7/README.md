![FastMVC](https://live.staticflickr.com/65535/52719951542_f745d984cc_o.png)  

# FastMVC
FastMVC is a web framework for building Web Applications
with the MVC structure (Model - View - Controller) and effortlessly deploying them to cloud platforms. 

- Model is interchangeable depending on the cloud platform you would like to use.
- View uses Jinja2 to create front end pages
- Controller is written using FastAPI


## FastMVC CLI
`fastmvc new [PROJECT_NAME]`  
Creates a new project. Will ask which platform to build towards (GOOGLE_APP_ENGINE, or DETA) and set up the base of the project accordingly.  

Optionally, you can pass the flag `--platform` and provide one of the options above.  

`fastmvc scaffold [MODEL_NAME] [ATTRIBUTE]:[DATA_TYPE]`  
Scaffold out a Model, View, and Controller for your object. For example:  

fastmvc scaffold post title:str content:wysiwyg draft:bool  

`fastmvc auth`  
Builds an Authentication Framework to easily integrate user sign in for your application.  

`fastmvc s`  
Alias for `uvicorn main:app --reload` to run your application locally  

## Supported Cloud Platforms
__Built__
- Google App Engine (using Firestore database)
- Deta (using DetaBase)

__Coming Soon__
- AWS Elastic Beanstalk


