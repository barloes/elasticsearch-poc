variable "name" {
}

variable "vpc_cidr" {
}

variable "availability_zone" {
  description = "Map from availability zone to the number that should be used for each availability zone's subnet"
  default = {
    "ap-southeast-1a" = 1
    "ap-southeast-1b" = 2
    "ap-southeast-1c" = 3
  }
}
