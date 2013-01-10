/*jslint bitwise: true, browser: true, eqeqeq: true, immed: true, newcap: true, regexp: true, nomen: false, onevar: false, undef: true, plusplus: false, white: true, indent: 2 */
/*global console module QUnit test */

QUnit.Django = {
  done: false,
  failedAssertions: [],
  moduleName: '',
  modules: {},
  original_module: module,
  original_test: test,
  ready: false,
  results: {modules: {}},
  screenshot_number: 1,
  testCases: {}
};

// Let us parse the test names from the page without running them; we'll start
// the tests manually when appropriate
QUnit.config.autostart = false;

// Hack the module and test definition functions so we can get information
// about the test queue before it's started.  Note that we'll be including
// even tests which won't be run due to a URL filter, if any.
module = function (name, testEnvironment) {
  QUnit.Django.moduleName = name;
  return QUnit.Django.original_module.apply(QUnit, arguments);
};

test = function (testName, expected, callback, async) {
  var qd = QUnit.Django,
      moduleName = qd.moduleName,
      modules = qd.modules;
  if (!(moduleName in modules)) {
      modules[moduleName] = [];
  }
  modules[moduleName].push(testName);
  return qd.original_test.apply(QUnit, arguments);
};

// Now collect the test results as the tests are run

QUnit.moduleStart(function (context) {
  // context = { name }
  var name = context.name,
      qd = QUnit.Django,
      modules = qd.results.modules;
  if (!name) {
    // Dummy module for a test that isn't contained in one
    name = '';
  }
  qd.moduleName = name;
  if (!(name in modules)) {
    modules[name] = {
      failed: 0,
      passed: 0,
      total: 0,
      tests: {},
      time: 0
    };
  }
});

QUnit.moduleDone(function (context) {
  // context = { name, failed, passed, total }
  var qd = QUnit.Django,
      results = qd.results.modules[context.name];
  results.failed = context.failed;
  results.passed = context.passed;
  results.total = context.total;
});

QUnit.testStart(function (context) {
  // context = { name, module }
  var qd = QUnit.Django,
      modules = qd.results.modules;
  qd.testStart = new Date();
  qd.failedAssertions = [];
});

QUnit.testDone(function (result) {
  // result = { name, failed, passed, total }
  var qd = QUnit.Django,
      module = qd.results.modules[qd.moduleName],
      time = (new Date() - qd.testStart) / 1000;
  module.tests[result.name] = {
    passed: result.passed,
    failed: result.failed,
    total: result.total,
    failedAssertions: qd.failedAssertions,
    time: time
  };
  module.passed += result.passed;
  module.failed += result.failed;
  module.total += result.total;
  module.time += time;
});

QUnit.log(function (details) {
  //details = { result, actual, expected, message }
  if (details.result) {
    return;
  }
  var qd = QUnit.Django,
      filename = "qunit_" + qd.screenshot_number + ".png",
      message = details.message || "";
  if (details.expected) {
    if (message) {
      message += ", ";
    }
    message = "expected: " + JSON.stringify(details.expected) + ", but was: " + JSON.stringify(details.actual);
  }
  qd.screenshot_number += 1;
  message += " (" + filename + ")";
  qd.failedAssertions.push(message);
  console.log("QUnit Screenshot:" + filename);
});

QUnit.done(function (details) {
  //details = { failed, passed, total, runtime }
  var qd = QUnit.Django,
      results = qd.results;
  results.failed = details.failed,
  results.passed = details.passed,
  results.total = details.total,
  results.time = details.runtime / 1000;
  qd.done = true;
});
