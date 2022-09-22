
#
# Configure the MongoDB Atlas Provider
#
terraform {
  required_providers {
    mongodbatlas = {
      source = "mongodb/mongodbatlas"
      version = "1.4.3"
    }
  }
}
provider "mongodbatlas" {
  public_key  = var.public_key
  private_key = var.private_key
}

provider "aws" {
  profile = "SA"
  region = "eu-north-1"
}


#
# Create a Shared Tier Cluster
#
resource "mongodbatlas_cluster" "pov-terraform" {
  project_id              = var.atlasprojectid
  name                    = "pov-terraform" 
  num_shards                   = 1
  replication_factor           = 3
  cloud_backup                 = true
  auto_scaling_disk_gb_enabled = var.auto_scaling_disk_gb_enabled
  mongo_db_major_version       = var.mongo_db_major_version

  //Provider settings
  provider_name               = var.atlas_provider_name
  provider_instance_size_name = var.atlas_provider_instance_size_name
  provider_region_name        = var.cluster_region
  }


resource "mongodbatlas_privatelink_endpoint" "pov-endpoint" {
  project_id    = var.atlasprojectid
  provider_name = var.atlas_provider_name
  region        = var.cluster_region
}

resource "aws_vpc_endpoint" "ptfe_service" {
  vpc_id             = "vpc-01c805bcda9b29b57"
  service_name       = mongodbatlas_privatelink_endpoint.pov-endpoint.endpoint_service_name
  vpc_endpoint_type  = "Interface"
  subnet_ids         = ["subnet-02c9862f9ed2b4a7c",  "subnet-057b552120127332c"]
  security_group_ids = ["sg-02ef6f2f7dc7a5f91"]
}

resource "mongodbatlas_privatelink_endpoint_service" "endpoint_service" {
  project_id          = mongodbatlas_privatelink_endpoint.pov-endpoint.project_id
  private_link_id     = mongodbatlas_privatelink_endpoint.pov-endpoint.private_link_id
  endpoint_service_id = aws_vpc_endpoint.ptfe_service.id
  provider_name       = var.atlas_provider_name
}

# Use terraform output to display connection strings.
output "connection_strings" {
value = ["${mongodbatlas_cluster.pov-terraform.connection_strings}"]
}
