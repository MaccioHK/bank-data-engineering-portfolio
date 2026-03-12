#!/bin/bash

for project in 0*; do
  for sub in "$project"/*; do
    if [ -d "$sub" ]; then
      touch "$sub/.gitkeep"
      echo "Created $sub/.gitkeep"
    fi
  done
done


