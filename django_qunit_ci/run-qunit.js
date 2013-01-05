/*jslint bitwise: true, browser: true, eqeqeq: true, immed: true, newcap: true, regexp: true, nomen: false, onevar: false, undef: true, plusplus: false, white: true, indent: 2 */
/*global $ setInterval console phantom WebPage */

if (phantom.args.length === 0) {
  console.log('Usage: run-qunit.js phantomjsServerPort [screenshotDir]');
  phantom.exit();
}

var phantomjsServerPort = phantom.args[0],
    screenshotDir = phantom.args[1],
    separator = require('fs').separator,
    server,
    service;

if (screenshotDir && screenshotDir.charAt(screenshotDir.length - 1) !== separator) {
  screenshotDir += separator;
}

function createPage() {
  var page = require('webpage').create();
  // Route "console.log()" calls from within the Page context to the main
  // Phantom context (i.e. current "this").  Also, generate screenshots when
  // requested
  page.onConsoleMessage = function (msg) {
    if (screenshotDir && msg.indexOf('QUnit Screenshot:') === 0) {
      page.render(screenshotDir + msg.slice(17));
    }
    else {
      console.log(msg);
    }
  };
  page.onError = function (msg, trace) {
    console.log(msg + ': ' + JSON.stringify(trace));
  };
  return page;
}

function waitFor(testFx, onReady, timeOutMillis) {
  var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 5001, //< Default Max Timout is 5s
    start = new Date().getTime(),
    condition = false,
    interval = setInterval(function () {
      if ((new Date().getTime() - start < maxtimeOutMillis) && !condition) {
        // If not time-out yet and condition not yet fulfilled
        condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
      } 
      else {
        if (!condition) {
          // If condition still not fulfilled (timeout but condition is 'false')
          console.log("'waitFor()' timeout");
          clearInterval(interval);
        } 
        else {
          // Condition fulfilled (timeout and/or condition is 'true')
          typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
          clearInterval(interval); //< Stop this interval
        }
      }
    }, 100); //< repeat check every 100 ms
}

// List the tests without actually running them.
function listTests(url, response) {
  var page = createPage(),
      responseText = '';
  page.open(url, function (status) {
    if (status === 'success') {
      responseText = page.evaluate(function () {
        try {
          return JSON.stringify(QUnit.Django.modules);
        }
        catch (e) {
          return '';
        }
      });
    }
    page.close();
    response.statusCode = responseText ? 200 : 500;
    response.write(responseText);
    response.close();
  });
}

function runTests(url, response) {
  var page = createPage();
      responseText = '';
  page.open(url, function (status) {
    if (status === 'success') {
      // Now that the page has loaded, start the tests
      page.evaluate(function () {
        QUnit.start();
      });
      // Wait for the tests to finish
      waitFor(function () {
        return page.evaluate(function () {
          return window.QUnit.Django && window.QUnit.Django.done;
        });
      }, function () {
        responseText = page.evaluate(function () {
          try {
            return JSON.stringify(QUnit.Django.results);
          }
          catch (e) {
            return '';
          }
        });
        page.close();
        response.statusCode = responseText ? 200 : 500;
        response.write(responseText);
        response.close();
      });
    }
    else {
      page.close();
      response.statusCode = 500;
      response.write('');
      response.close();
    }
  });
}

// Start the web server that listens for requests from the Django test suite
server = require('webserver').create();
service = server.listen(phantomjsServerPort, function (request, response) {
  var params;
  if (request.method === 'GET') {
    // Just making sure the server's running
    response.statusCode = 200;
    response.write('');
    response.close();
    return;
  }
  params = JSON.parse(request.post);
  if (params.action === 'list') {
    listTests(params.url, response);
  }
  else {
    runTests(params.url, response);
  }
});
