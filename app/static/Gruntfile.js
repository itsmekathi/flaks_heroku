module.exports = function (grunt) {
    grunt.initConfig({
        uglify: {
            options: {
            },
            libraries: {
                files: {
                    // Bundle all the libraries which are not pointing to cdn.
                    'scripts/distribution/libraries.min.js':
                        [
                            'scripts/distribution/libraries/angular-chart.min.js'
                        ]
                }
            },
            angular_files: {
                files: {
                    // Bundle the module, directives and shared services into one file
                    'scripts/distribution/app.module.min.js':
                        [
                            'scripts/app/app.module.js',
                            'scripts/app/directives/currentTime.directive.js',
                            'scripts/app/directives/httprequest.directive.js',
                            'scripts/app/directives/modal.directive.js',
                            'scripts/app/directives/simpleModal.directive.js',
                            'scripts/app/sharedservices/modal.service.js',
                            'scripts/app/sharedservices/toastr.service.js',
                            'scripts/app/sharedservices/ui.modal.service.js',
                        ]
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Default task.
    grunt.registerTask('minify', ['uglify']);

};
