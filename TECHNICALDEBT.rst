Technical Debt
==============
| The list below represent our technical debt which we will be addressed in the coming future
| We will check the debt which is done by a |done| 


Enable Git Action for Continuous Integration and Delivery(CI/CD)
----------------------------------------------------------------
Upon merge into **develop** branch, a test,test coverage report, deploy to docker and pypi test should happen with no error


Apply the rule for PR merging
------------------------------
Merge to **develop** branch should have a rule of merge like checks against certain criteria to be fulfilled


Implement push rule to protect the master branch from any misuse
----------------------------------------------------------------
 **master** or **main** branch should be protected against any misuse. The 
 merge to **master** should automatically release to production and there should be strict rules to prevent
 any bug into production release 


Populate the test coverage link with the write test coverage report
-------------------------------------------------------------------
The test coverage report should be published upon release on test as well as on production


Include python version 313 in tox once it comes up in production
----------------------------------------------------------------
Once this version comes as production version, we need to include it in tox file to be able to be compatible with it 


.. |done| image::  https://img.shields.io/badge/DONE-green
            :alt: DONE

Known issue
-----------
Background of the dmc-view app is being affected by the system's theme (light/dark). It is hard to read the values in dark theme.


IDE friendly API doc popup
--------------------------
When hovering over a method in VS, it should show a popup with the method input and output parameters.
At the bottom it should show API doc explaining the method.