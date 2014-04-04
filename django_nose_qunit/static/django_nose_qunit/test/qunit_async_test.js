/*global raw_script */
QUnit.Django.start();

asyncTest("asyncTest() should work correctly", function () {
  expect(1);
  setTimeout(function () {
    // Only care that this made it into the results at all
    ok(true);
    start();
  }, 200);
});

QUnit.Django.end();
