var jshint = require("gulp-jshint");
var gulp = require('gulp');
var src = './scripts/app/';

gulp.task('lint', function () {
    return gulp.src(src + '**/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});
