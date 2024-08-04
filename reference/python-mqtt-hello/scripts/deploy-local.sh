#!/bin/bash

# Navigate to the script's directory
echo "Navigating to the script's directory..."
cd "$(dirname "$0")"/..

# Build the component
echo "Building the Greengrass component..."
gdk component build

# Create deployment and capture the output and status
echo "Creating deployment..."
DEPLOYMENT_OUTPUT=$(sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir $PWD/greengrass-build/recipes \
  --artifactDir $PWD/greengrass-build/artifacts \
  --merge "com.example.PythonMqttHello=1.0.0" 2>&1)
DEPLOYMENT_STATUS=$?

# Check if the deployment failed
if [ $DEPLOYMENT_STATUS -ne 0 ]; then
  echo "Deployment failed. Output:"
  echo "$DEPLOYMENT_OUTPUT"

  # Extract deployment ID from the output
  echo "Extracting deployment ID from the output..."
  DEPLOYMENT_ID=$(echo "$DEPLOYMENT_OUTPUT" | grep -oP '(?<=Deployment Id: )[^ ]+')

  if [ -n "$DEPLOYMENT_ID" ]; then
    echo "Removing failed deployment with ID: $DEPLOYMENT_ID"
    sudo /greengrass/v2/bin/greengrass-cli deployment delete --deploymentId $DEPLOYMENT_ID
  else
    echo "Failed to extract deployment ID from the output."
  fi

  exit 1
else
  echo "Deployment succeeded."
  exit 0
fi
