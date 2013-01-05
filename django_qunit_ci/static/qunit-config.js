/*jslint bitwise: true, browser: true, eqeqeq: true, immed: true, newcap: true, regexp: true, nomen: false, onevar: false, undef: true, plusplus: false, white: true, indent: 2 */
/*global console QUnit */

QUnit.Django = {
  done: false,
  failedAssertions: [],
  moduleName: '',
  modules: {},
  results: {modules: {}},
  screenshot_number: 1,
  testCases: {}
};

console.error = console.warn = function () {};

// Let us parse the test names from the page without running them; we'll start
// the tests manually when appropriate
QUnit.config.autostart = false;

// Hack the module and test definition functions so we can get information
// about the test queue before it's started.  Note that we'll be including
// even tests which won't be run due to a URL filter, if any.
QUnit.Django.original_module = module;

module = function (name, testEnvironment) {
  QUnit.Django.moduleName = name;
  return QUnit.Django.original_module.apply(QUnit, arguments);
};

QUnit.Django.original_test = test;

test = function (testName, expected, callback, async) {
  if (!(QUnit.Django.moduleName in QUnit.Django.modules)) {
      QUnit.Django.modules[QUnit.Django.moduleName] = [];
  }
  QUnit.Django.modules[QUnit.Django.moduleName].push(testName);
  return QUnit.Django.original_test.apply(QUnit, arguments);
};

// Now collect the test results as the tests are run

QUnit.moduleStart(function (context) {
  // context = { name }
  QUnit.Django.moduleStart = new Date();
  QUnit.Django.testCases = {};
});

QUnit.moduleDone(function (context) {
  // context = { name, failed, passed, total }
  QUnit.Django.results.modules[context.name] = {
    failed: context.failed,
    passed: context.passed,
    total: context.total,
    tests: QUnit.Django.testCases,
    time: (new Date() - QUnit.Django.moduleStart) / 1000
  };
});

QUnit.testStart(function (context) {
  // context = { name, module }
  QUnit.Django.testStart = new Date();
  QUnit.Django.failedAssertions = [];
});

QUnit.testDone(function (result) {
  // result = { name, failed, passed, total }
  var module,
      time = (new Date() - QUnit.Django.testStart) / 1000;
  QUnit.Django.testCases[result.name] = {
    passed: result.passed,
    failed: result.failed,
    total: result.total,
    failedAssertions: QUnit.Django.failedAssertions,
    time: time
  };
  if (QUnit.Django.moduleName == '') {
    // Build a pseudo-module for tests that aren't contained in one
    if (!('' in QUnit.Django.results.modules)) {
      QUnit.Django.results.modules[''] = {
        passed: 0,
        failed: 0,
        total: 0,
        time: 0,
        tests: QUnit.Django.testCases
      }
    }
    module = QUnit.Django.results.modules[''];
    module.passed += result.passed;
    module.failed += result.failed;
    module.total += result.total;
    module.time += time;
  }
});

QUnit.log(function (details) {
  //details = { result, actual, expected, message }
  if (details.result) {
    return;
  }
  var filename = "qunit_" + QUnit.Django.screenshot_number + ".png",
      message = details.message || "";
  if (details.expected) {
    if (message) {
      message += ", ";
    }
    message = "expected: " + JSON.stringify(details.expected) + ", but was: " + JSON.stringify(details.actual);
  }
  QUnit.Django.screenshot_number += 1;
  message += " (" + filename + ")";
  QUnit.Django.failedAssertions.push(message);
  console.log("QUnit Screenshot:" + filename);
});

QUnit.done(function (details) {
  //details = { failed, passed, total, runtime }
  QUnit.Django.results.failed = details.failed,
  QUnit.Django.results.passed = details.passed,
  QUnit.Django.results.total = details.total,
  QUnit.Django.results.time = details.runtime / 1000;
  QUnit.Django.done = true;
});
