#!/bin/bash
# run unit and integration tests INSIDE the docker container
source ./install/setup.bash
# TODO: move unit tests to an own folder
echo ""
echo "-- starting unit tests using colcon --"
echo ""
colcon test --pytest-with-coverage --event-handlers console_cohesion+  --return-code-on-test-failure
echo ""
echo "-- starting integration tests using launch_test --"
echo ""
# Note that you need to define each test individually
launch_test src/mapdesc_ros/integration_tests/launch_testing/marker_launch_test.py