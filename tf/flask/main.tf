// Configure the Google Cloud provider
provider "google" {
// do not use json file. just use gcloud credentials
// credentials = file("CREDENTIALS_FILE.json")
 project     = var.project
 region      = var.region
}

// Terraform plugin for creating random ids
resource "random_id" "instance_id" {
 byte_length = 8
}

// A single Compute Engine instance
resource "google_compute_instance" "default" {
 name         = "flask-vm-${random_id.instance_id.hex}"
 machine_type = var.machine_type
 zone         = var.zone

 boot_disk {
   initialize_params {
     image = "debian-cloud/debian-10"
   }
 }

// Make sure flask is installed on all new instances for later steps
 metadata_startup_script = <<SCRIPT
sudo apt-get update
sudo apt-get install -yq build-essential python-pip rsync wget
pip install flask
SCRIPT

 network_interface {
   network = "default"

   access_config {
     // Include this section to give the VM an external ip address
   }
 }

 metadata = {
   ssh-keys = "${var.ssh_user}:${file("~/.ssh/id_rsa.pub")}"
 }
}

output "ip" {
   value =  google_compute_instance.default.network_interface.0.access_config.0.nat_ip
}

resource "google_compute_firewall" "default" {
 name    = "flask-app-firewall"
 network = "default"

 allow {
   protocol = "tcp"
   ports    = ["5000"]
 }
}
