require 'json'
require 'yaml'

# Function to print usage instructions
def print_usage
  puts "Usage: ruby json2yaml.rb <input_json_file> <output_yaml_file>"
end

# Check for the correct number of arguments
if ARGV.length != 2
  puts "Error: Incorrect number of arguments."
  print_usage
  exit
end

json_file_name, yaml_file_name = ARGV

# Check if the JSON file exists
unless File.exist?(json_file_name)
  puts "Error: JSON file '#{json_file_name}' not found."
  exit
end

# Load JSON data from the specified file
file = File.read(json_file_name)
begin
  data = JSON.parse(file)
rescue JSON::ParserError => e
  puts "Error parsing JSON file: #{e.message}"
  exit
end

# Convert the data to YAML
yaml_data = data.to_yaml

# Write the YAML data to the specified file
File.open(yaml_file_name, 'w') { |file| file.write(yaml_data) }

puts "Successfully converted '#{json_file_name}' to '#{yaml_file_name}'"
