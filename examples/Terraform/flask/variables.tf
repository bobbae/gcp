variable "project" {
   type = string
}

variable "region" {
   type = string
   default = "us-central1"
}

variable "zone" {
   type = string
   default = "us-central1-c"
}

variable "machine_type" {
   type = string
   default = "f1-micro"
}

variable "ssh_user" {
   type = string
   default = "bob"
}
