/*jslint bitwise: true, browser: true, eqeqeq: true, immed: true, newcap: true, regexp: true, nomen: false, onevar: false, undef: true, plusplus: false, white: true, indent: 2 */
/*global console QUnit */

// This is our one addition to the page's global namespace
var DjangoQUnit = {
  done: false,
  failedAssertions: [],
  modules: [],
  results: [modules: []],
  screenshot_number: 1,
  testCases: [];
};

console.error = console.warn = function () {};

// Let us parse the test names from the page without running them; we'll start
// the tests manually when appropriate
QUnit.config.autostart = false;

// Hack the module and test definition functions so we can get information
// about the test queue before it's started.  Note that we'll be including
// even tests which won't be run due to a URL filter, if any.
QUnit.original_module = QUnit.module;

QUnit.module = function (name, testEnvironment) {
  DjangoQUnit.modules.push({name: name, tests: []});
  return QUnit.original_module(name, testEnvironment);
};

QUnit.original_test = QUnit.test;

QUnit.test = function (testName, expected, callback, async) {
  if (DjangoQUnit.modules.length === 0) {
      // Top-level test, add a dummy module for it
      DjangoQUnit.modules.push({name: '', tests: []});
  }
  DjangoQUnit.modules[DjangoQUnit.modules.length - 1].push(testName);
  return QUnit.original_test(testName, expected, callback, async);
};

// Now collect the test results as the tests are run

QUnit.moduleStart(function (context) {
  // context = { name }
  DjangoQUnit.moduleStart = new Date();
  DjangoQUnit.testCases = [];
});

QUnit.moduleDone(function (context) {
  // context = { name, failed, passed, total }
  DjangoQUnit.results.modules.push({
    name: context.name ? context.name : '',
    errors: 0,
    failures: context.failed,
    tests: DjangoQUnit.testCases,
    time: (new Date() - DjangoQUnit.moduleStart) / 1000,
  });
});

QUnit.testStart(function (context) {
  // context = { name, module }
  DjangoQUnit.testStart = new Date();
  DjangoQUnit.failedAssertions = [];
});

QUnit.testDone(function (result) {
  // result = { name, failed, passed, total }
  DjangoQUnit.testCases.push({
    name: result.name,
    passed: result.passed,
    failed: result.failed,
    failedAssertions: DjangoQUnit.failedAssertions,
    time: (new Date() - DjangoQUnit.testStart) / 1000
  });
});

QUnit.log(function (details) {
  //details = { result, actual, expected, message }
  if (details.result) {
    return;
  }
  var filename = "qunit_" + DjangoQUnit.screenshot_number + ".png",
      message = details.message || "";
  if (details.expected) {
    if (message) {
      message += ", ";
    }
    message = "expected: " + JSON.stringify(details.expected) + ", but was: " + JSON.stringify(details.actual);
  }
  DjangoQUnit.screenshot_number += 1;
  message += " (" + filename + ")";
  DjangoQUnit.failedAssertions.push(message);
  console.log("QUnit Screenshot:" + filename);
});

QUnit.done(function (details) {
  //details = { failed, passed, total, runtime }
  DjangoQUnit.results.failed = failed,
  DjangoQUnit.results.passed = passed,
  DjangoQUnit.results.total = total,
  DjangoQUnit.results.time = runtime / 1000;
  DjangoQUnit.done = true;
});
