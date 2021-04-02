# Specify the GCP Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

