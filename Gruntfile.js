/*global module: false */
module.exports = function (grunt) {

  var jenkins = grunt.option('jenkins'),
      jshint_config,
      jshint_tests_config;
  jshint_config = {
    ignores: ['django_nose_qunit/static/qunit.js'],
    jshintrc: '.jshintrc'
  };
  jshint_tests_config = {
    jshintrc: 'django_nose_qunit/static/django_nose_qunit/test/.jshintrc'
  };
  if (jenkins) {
    jshint_config.reporter = 'jslint';
    jshint_config.reporterOutput = 'jshint.xml';
    jshint_tests_config.reporterOutput = 'jshint_tests.xml';
  }

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      all: ['Gruntfile.js', 'django_nose_qunit/static/*.js'],
      options: jshint_config,
      tests: {
        src: ['django_nose_qunit/static/django_nose_qunit/test/*.js'],
        options: jshint_tests_config
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('default', ['jshint']);

};
