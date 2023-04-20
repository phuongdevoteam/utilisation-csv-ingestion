variable "project_id" {
  type        = string
  description = "The projects to create directly under this folder"
}

variable "billing_account" {
  type        = string
  description = "The billing account the project will be linked to"
}

variable "folder_id" {
  type        = string
  description = "The numeric ID of the folder this project should be created under, without folder/ prefix"
  default     = null
}

variable "project_number" {
  type        = number
  description = "Project Number"
}

variable "cloud_composer_name" {
  type        = string
  description = "Name of the Cloud Composer environment"
}

variable "cloud_composer_region" {
  type        = string
  description = "Region where the cloud composer environment is hosted."
  # TODO: how can I validate this? keep track of all the locations avaiable by google?
}

variable "software_config" {
  type = object({
    airflow_config_overrides = map(string),
    image_version            = string,
    pypi_packages            = map(string),
    env_variables            = map(string)
  })
  default = {
    airflow_config_overrides = null
    env_variables            = null
    image_version            = "composer-2.0.0-preview.4-airflow-2.1.2"
    pypi_packages            = null
  }
  # TODO:
  # descriptions:
  # pypi_packages: Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. \"numpy\"). Values are the lowercase extras and version specifier."
  # image version: "(Optional in Cloud Composer 1, required in Cloud Composer 2) The version of the software running in the environment."
}

variable "cloud_function_service_account" {
  type        = string
  description = "A service account string and its display name"
  default     = ""
}

variable "bucket_name" {
  type        = string
  description = "Name of the bucket created by this terraform module. You can select a region, dual-region, or multi-region."
  # TODO: how can I validate this? keep track of all the locations avaiable by google?
}
