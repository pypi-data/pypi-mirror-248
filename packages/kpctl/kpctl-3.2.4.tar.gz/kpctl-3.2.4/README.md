kpctl
=====

Command line interface to:

- inspect, document, enhance and validate BPMN files; and
- execute process-based applications on the KnowProcess platform

Build and publish to PyPI
-----------------------------------------

1. Increment version

   ```
   poetry version [major|minor|patch]
   ```

2. Build...

   ```
   poetry build
   ```

3. Test

   ```
   poetry run tests
   ```

4. Publish to PyPi production server (cannot be repeated for same version)

   ```
   poetry publish --build
   ```
